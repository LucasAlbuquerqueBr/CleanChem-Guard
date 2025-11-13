import os
import uuid
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, current_app
from flask_login import LoginManager, current_user

from config import Config
from i18n import init_i18n, t, set_lang_from_request, get_current_lang
from sheets_db import SheetsDB
from models import User


login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    db = SheetsDB.get()
    data = db.get_user_by_id(user_id)
    if not data:
        return None
    return User.from_record(data)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Init i18n
    init_i18n(app)

    # Init DB (Google Sheets)
    SheetsDB.init(app)

    # Login manager
    login_manager.init_app(app)

    # Blueprints
    from blueprints.auth import bp as auth_bp
    from blueprints.gallery import bp as gallery_bp
    from blueprints.chat import bp as chat_bp
    from blueprints.ai import bp as ai_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(ai_bp)

    @app.before_request
    def _set_lang():
        # Ensure translations are up-to-date and language set
        try:
            # Re-init i18n lightly to catch JSON changes without restart
            init_i18n(current_app)
        except Exception:
            pass
        set_lang_from_request()

    @app.context_processor
    def inject_globals():
        # Active section helper
        ep = (request.endpoint or "")
        if ep.startswith("gallery."):
            active = "gallery"
        elif ep.startswith("chat."):
            active = "chats"
        elif ep.startswith("ai."):
            active = "ai"
        elif ep.startswith("auth."):
            active = "auth"
        elif ep == "index":
            active = "home"
        else:
            active = ""

        # Unread chats count
        unread = 0
        try:
            if current_user.is_authenticated:
                unread = SheetsDB.get().count_unread_chats_for_user(str(current_user.id))
        except Exception:
            unread = 0

        return {
            "_": t,
            "current_lang": get_current_lang(),
            "current_user": current_user,
            "active_section": active,
            "unread_chats": unread,
        }

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/uploads/<path:filename>")
    def uploads(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
