from flask import Blueprint, render_template, request, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user

from sheets_db import SheetsDB
from i18n import t


bp = Blueprint("chat", __name__, url_prefix="/chat")


@bp.get("/")
@login_required
def list_chats():
    db = SheetsDB.get()
    chats = db.list_chats_for_user(current_user.id)
    # Resolve partner usernames
    users_by_id = {}
    def uname(uid):
        if uid not in users_by_id:
            users_by_id[uid] = db.get_user_by_id(uid)
        u = users_by_id[uid]
        return u.get("username") if u else "?"
    items = []
    for c in chats:
        partner = c["user1_id"] if c["user2_id"] == current_user.id else c["user2_id"]
        items.append({"id": c["id"], "partner": uname(partner), "created_at": c.get("created_at")})
    return render_template("chat_list.html", chats=items)


@bp.post("/start")
@login_required
def start_chat():
    username = request.form.get("username", "").strip()
    db = SheetsDB.get()
    target = db.get_user_by_username(username)
    if not target:
        return redirect(url_for("chat.list_chats"))
    chat = db.get_or_create_chat(current_user.id, target["id"])
    return redirect(url_for("chat.chat_room", chat_id=chat["id"]))


def _ensure_member(chat: dict):
    return chat and (chat.get("user1_id") == current_user.id or chat.get("user2_id") == current_user.id)


@bp.get("/<chat_id>")
@login_required
def chat_room(chat_id):
    db = SheetsDB.get()
    chat = db.get_chat(chat_id)
    if not _ensure_member(chat):
        abort(404)
    partner_id = chat["user1_id"] if chat["user2_id"] == current_user.id else chat["user2_id"]
    partner = db.get_user_by_id(partner_id)
    # Mark as read for current user when opening the room
    try:
        db.set_last_read(chat_id, str(current_user.id))
    except Exception:
        pass
    return render_template("chat_room.html", chat=chat, partner=partner)


@bp.get("/api/<chat_id>/messages")
@login_required
def api_messages(chat_id):
    db = SheetsDB.get()
    chat = db.get_chat(chat_id)
    if not _ensure_member(chat):
        abort(404)
    since = request.args.get("since")
    msgs = db.list_messages(chat_id, since)
    return jsonify({"messages": msgs})


@bp.post("/api/<chat_id>/messages")
@login_required
def api_send_message(chat_id):
    db = SheetsDB.get()
    chat = db.get_chat(chat_id)
    if not _ensure_member(chat):
        abort(404)
    content = request.json.get("content", "").strip()
    if not content:
        return jsonify({"ok": False}), 400
    msg = db.add_message(chat_id, current_user.id, content)
    return jsonify({"ok": True, "message": msg})
