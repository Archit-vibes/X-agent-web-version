from flask import Blueprint, jsonify, session
import time
import requests

from backend.db import SessionLocal
from backend.models import Reply
from auth.storage import user_tokens

posting_bp = Blueprint("posting", __name__, url_prefix="/api/posting")

url = "https://api.x.com/2/tweets"


@posting_bp.route("/auto-post", methods=["POST"])
def auto_post():

    x_user_id = session.get("x_user_id")
    token_data = user_tokens.get(x_user_id)

    if not token_data:
        return jsonify({"error": "Not authenticated"}), 401
    

    token = token_data["access_token"]

    db = SessionLocal()

    try:
        replies = (
            db.query(Reply)
            .filter(Reply.status == "generated")
            .limit(3)
            .all()
        )

        if not replies:
            return jsonify({"message": "No replies to post"}), 200

        posted = []

        for reply in replies:
            try:


                payload = {
                    "reply": { "in_reply_to_tweet_id": f"{reply.target_tweet_id}" },
                    "text": f"{reply.reply_text}"
                }

                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }

                response = requests.post(url, json=payload, headers=headers)

                print(response.status_code)
                print(response.json())


                reply.status = "posted"
                db.commit()
                posted.append(reply.id)

                time.sleep(15)

            except Exception as e:
                db.rollback()
                reply.status = "failed"
                db.commit()
                print(f"Failed to post reply {reply.id}: {e}")

        return jsonify({
            "posted_count": len(posted),
            "posted_reply_ids": posted
        })

    finally:
        db.close()

