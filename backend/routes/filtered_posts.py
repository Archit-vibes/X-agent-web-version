from flask import Blueprint, jsonify
from sqlalchemy.exc import IntegrityError

from services.filtering import build_vectorizer, hybrid_score
from backend.db import SessionLocal
from backend.models import Post, FilteredPost

filtered_bp = Blueprint("filtered", __name__, url_prefix="/api/posts")


@filtered_bp.route("/filtered")
def filtered_posts():
    db = SessionLocal()

    try:
        posts = db.query(Post).all()

        if not posts:
            return jsonify([])

        corpus = [p.text for p in posts]

        query = "hiring internship job opening engineer developer"

        vectorizer, query_vec = build_vectorizer(corpus)

        results = []

        for post in posts:
            score = hybrid_score(post.text, vectorizer, query_vec)

            if score < 0.03:
                continue

            filtered = FilteredPost(
                id=post.id,
                text=post.text,
                author_id=post.author_id,
                score=round(score * 100, 2),
            )

            try:
                db.add(filtered)
                db.commit()
            except IntegrityError:
                db.rollback()

            results.append({
                "id": filtered.id,
                "text": filtered.text,
                "author_id": filtered.author_id,
                "score": filtered.score,
            })

        return jsonify(results)

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()
