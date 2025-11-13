import os
import uuid
from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from flask_login import login_required, current_user

from i18n import t
from sheets_db import SheetsDB


bp = Blueprint("gallery", __name__, url_prefix="/gallery")


@bp.route("/", methods=["GET"])
@login_required
def gallery_index():
    db = SheetsDB.get()
    tag = request.args.get("tag")
    q = request.args.get("q")
    subject = request.args.get("subject")
    posts = db.list_posts(tag=tag, q=q, subject=subject)
    return render_template("gallery.html", posts=posts)


def _allowed(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


@bp.route("/upload", methods=["POST"])
@login_required
def upload():
    file = request.files.get("file")
    content = request.form.get("content", "")
    tags = request.form.get("tags", "")
    description = request.form.get("description", "")
    subject = request.form.get("subject", "")
    if not file or file.filename == "":
        flash(t("gallery.no_file"))
        return redirect(url_for("gallery.gallery_index"))
    if not _allowed(file.filename):
        flash(t("gallery.invalid_type"))
        return redirect(url_for("gallery.gallery_index"))
    os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
    ext = file.filename.rsplit(".", 1)[-1].lower()
    fid = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], fid)
    file.save(path)
    media_url = url_for("uploads", filename=fid)
    media_type = "video" if ext in {"mp4", "mov", "webm"} else "image"
    db = SheetsDB.get()
    db.create_post(
        author_id=str(getattr(current_user, "id")),
        content=content,
        media_url=media_url,
        media_type=media_type,
        tags=tags,
        description=description,
        subject=subject,
    )
    flash(t("gallery.upload_success"))
    return redirect(url_for("gallery.gallery_index"))
