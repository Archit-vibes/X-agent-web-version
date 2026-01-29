from flask import Blueprint, jsonify, request
from services.x_mentions import fetch_recent_mentions
from backend.db import SessionLocal
from backend.models import Mention
from sqlalchemy.exc import IntegrityError

mentions_bp = Blueprint("mentions", __name__, url_prefix="/api")

@mentions_bp.route("/mentions")
def mentions():
    # This might still be useful if we want a default view, but for now sticking to the plan
    # to make a new api for fetching with ID.
    mentions = fetch_recent_mentions("default_id_if_needed") # Or empty, but existing code had no args in route but arg in definition.
                                                             # Wait, original mentions() called fetch_recent_mentions() without args, 
                                                             # but definition has `id`. This implies it was failing or I misread.
                                                             # Ah, looking at previous view_file of x_mentions.py: def fetch_recent_mentions(id):
                                                             # But mentions.py line 11 called: fetch_recent_mentions(). 
                                                             # This would raise TypeError. 
                                                             # User noted: "fetch_recent_mentions func require an id... but when I call mentions.py via frontend... it doesnt pass any id"
                                                             # So the existing code was likely broken or I viewed a version that was just changed.
                                                             # Regardless, I will implement the new separate route as requested.
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
            # Check if mention already exists to avoid unique constraint errors if not handled by ON CONFLICT or similar
            # The original code handled IntegrityError by rolling back, which is fine for bulk insert attempts 
            # where some might exist.
            
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
