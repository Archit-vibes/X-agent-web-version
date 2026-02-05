import os

from flask import Blueprint, request, jsonify, redirect, session
import secrets, base64, hashlib , requests

from backend.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTH_URL, TOKEN_URL
from auth.storage import user_tokens

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login')
def login():
    state = secrets.token_urlsafe(16)
    session["state"] = state

    code_verifier = secrets.token_urlsafe(40)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b'=').decode()

    session["code_verifier"] = code_verifier

    auth_params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "tweet.read tweet.write users.read offline.access",
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    auth_url = f"{AUTH_URL}?{'&'.join(f'{k}={v}' for k,v in auth_params.items())}"
    return redirect(auth_url)



@auth_bp.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")

    if not code or state != session.get("state"):
        return "Invalid state or missing code", 400

    code_verifier = session.get("code_verifier")
    if not code_verifier:
        return "Missing code verifier", 400

    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}",
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": code_verifier,
    }

    token_response = requests.post(TOKEN_URL, data=data, headers=headers)

    if token_response.status_code != 200:
        return jsonify({
            "error": "Token exchange failed",
            "details": token_response.text
        }), 500

    token_json = token_response.json()

    user_headers = {
        "Authorization": f"Bearer {token_json['access_token']}"
    }

    me_response = requests.get(
        "https://api.x.com/2/users/me",
        headers=user_headers
    )

    if me_response.status_code != 200:
        return jsonify({
            "error": "Failed to fetch user identity",
            "details": me_response.text
        }), 500

    x_user_id = me_response.json()["data"]["id"]


    session.clear() 
    session["x_user_id"] = x_user_id

    user_tokens[x_user_id] = {
        "access_token": token_json["access_token"],
        "refresh_token": token_json.get("refresh_token"),
    }

    print("SESSION:", dict(session))
    print("TOKENS:", user_tokens.keys())

    return redirect("http://localhost:5173/dashboard")


@auth_bp.route("/check")
def check_auth():
    x_user_id = session.get("x_user_id")

    is_authenticated = (
        x_user_id is not None
        and x_user_id in user_tokens
    )

    return jsonify({"authenticated": is_authenticated})


@auth_bp.route("/logout")
def logout():
    uid = session.get("user_id")
    if uid in user_tokens:
        del user_tokens[uid]
    session.clear()
    return jsonify({"success": True})

