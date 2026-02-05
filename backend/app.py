import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from flask_session import Session
from flask_cors import CORS
from auth.routes import auth_bp
from routes.posts import posts_bp
from routes.mentions import mentions_bp
from routes.filtered_posts import filtered_bp
from routes.replies import replies_bp
from routes.posting import posting_bp
from db import Base, engine


Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.secret_key = "dev-secret"

app.config.update(
    SESSION_TYPE="filesystem",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)


CORS(
    app,
    supports_credentials=True,
    origins=["http://localhost:5173"]
)

Session(app)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(posts_bp)
app.register_blueprint(mentions_bp)
app.register_blueprint(filtered_bp)

app.register_blueprint(replies_bp)
app.register_blueprint(posting_bp)


if __name__ == "__main__":
    app.run(debug=True)
