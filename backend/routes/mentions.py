from flask import Blueprint, jsonify, request
from services.x_mentions import fetch_recent_mentions
from backend.db import SessionLocal
from backend.models import Mention
from sqlalchemy.exc import IntegrityError

mentions_bp = Blueprint("mentions", __name__, url_prefix="/api")

@mentions_bp.route("/mentions")
def mentions():
    mentions = fetch_recent_mentions()
    return jsonify([])

@mentions_bp.route("/fetch_mentions", methods=["POST"])
def fetch_mentions_api():
    data = request.get_json()
    user_id = data.get("id")
    
    if not user_id:
        return jsonify({"error": "ID is required"}), 400

    mentions = fetch_recent_mentions(user_id)

    db = SessionLocal()
    
    try:
        for mention_dict in mentions:
            
            mention = Mention(
                id=int(mention_dict['id']),
                text=mention_dict['text'],
                author_id=mention_dict.get('author_id')
            )

            db.add(mention)
            print(f"Saved mention ID {mention.id} to database.")

        db.commit()

    except IntegrityError:
            db.rollback()
            print(f"Post ID already exists in the database. Skipping.******************************************************")

    except Exception as e:
            db.rollback()
            print(f"Error occurred: {e}--------------------------------------------")

    finally:
        db.close()

    return jsonify(mentions)
