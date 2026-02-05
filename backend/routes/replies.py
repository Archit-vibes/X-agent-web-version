from flask import Blueprint, jsonify
from backend.db import SessionLocal
from backend.models import Reply
from services.llm import generate_replies_for_filtered_posts

replies_bp = Blueprint("replies", __name__, url_prefix="/api/replies")

@replies_bp.route("/generate", methods=["POST"])
def generate_replies():
    try:
        new_replies = generate_replies_for_filtered_posts()
        return jsonify({"message": "Replies generated successfully", "count": len(new_replies), "replies": new_replies}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@replies_bp.route("/list", methods=["GET"])
def list_replies():
    db = SessionLocal()
    try:
        replies = db.query(Reply).all()
        results = [
            {
                "id": r.id,
                "post_text": r.post_text,
                "reply_text": r.reply_text
            }
            for r in replies
        ]
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
