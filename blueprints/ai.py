from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from openai import OpenAI

from i18n import t
from config import Config


bp = Blueprint("ai", __name__, url_prefix="/ai")


@bp.get("/")
@login_required
def ai_page():
    return render_template("ai_chat.html")


@bp.post("/api/chat")
@login_required
def ai_chat():
    data = request.get_json() or {}
    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "empty"}), 400
    cfg = Config()
    if not cfg.OPENAI_API_KEY:
        return jsonify({"error": "OpenAI API key not configured"}), 500
    client = OpenAI(api_key=cfg.OPENAI_API_KEY)
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a small social app."},
                {"role": "user", "content": user_message},
            ],
        )
        text = resp.choices[0].message.content
        return jsonify({"reply": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

