import json
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import gspread
from google.oauth2.service_account import Credentials


class SheetsDB:
    _instance: Optional["SheetsDB"] = None

    @classmethod
    def init(cls, app):
        if cls._instance is None:
            cls._instance = SheetsDB(app)

    @classmethod
    def get(cls) -> "SheetsDB":
        if cls._instance is None:
            raise RuntimeError("SheetsDB not initialized")
        return cls._instance

    def __init__(self, app):
        self.app = app
        self.gc = self._auth_client(
            app.config.get("GOOGLE_APPLICATION_CREDENTIALS"),
            app.config.get("GOOGLE_SHEETS_CREDS_JSON"),
        )
        spreadsheet_id = app.config.get("GOOGLE_SHEETS_SPREADSHEET_ID")
        if spreadsheet_id:
            self.spread = self.gc.open_by_key(spreadsheet_id)
        else:
            name = app.config.get("GOOGLE_SHEETS_SPREADSHEET_NAME", "CleanChem Social")
            self.spread = self.gc.open(name)

        self.users_ws = self._ensure_ws("users", [
            "id", "username", "email", "password_hash", "avatar_url", "bio", "created_at"
        ])
        self.posts_ws = self._ensure_ws("posts", [
            "id", "author_id", "content", "media_url", "media_type", "tags", "description", "subject", "created_at"
        ])
        self.chats_ws = self._ensure_ws("chats", [
            "id", "user1_id", "user2_id", "created_at"
        ])
        self.messages_ws = self._ensure_ws("messages", [
            "id", "chat_id", "sender_id", "content", "created_at"
        ])
        self.chat_reads_ws = self._ensure_ws("chat_reads", [
            "id", "chat_id", "user_id", "last_read_at"
        ])

    def _auth_client(self, path: Optional[str], json_str: Optional[str]):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        if json_str:
            info = json.loads(json_str)
            creds = Credentials.from_service_account_info(info, scopes=scopes)
        elif path:
            creds = Credentials.from_service_account_file(path, scopes=scopes)
        else:
            raise RuntimeError("Google Sheets credentials not configured. Set GOOGLE_SHEETS_CREDS_JSON or GOOGLE_APPLICATION_CREDENTIALS.")
        return gspread.authorize(creds)

    def _ensure_ws(self, title: str, headers: List[str]):
        try:
            ws = self.spread.worksheet(title)
        except gspread.WorksheetNotFound:
            ws = self.spread.add_worksheet(title=title, rows=100, cols=len(headers))
            ws.append_row(headers)
            return ws
        # ensure headers
        current = ws.row_values(1)
        if current != headers:
            if not current:
                ws.append_row(headers)
            else:
                ws.update(f"A1:{chr(64+len(headers))}1", [headers])
        return ws

    # Utility
    def _get_all(self, ws) -> List[Dict[str, Any]]:
        return ws.get_all_records()

    def _append(self, ws, headers: List[str], record: Dict[str, Any]):
        row = [str(record.get(h, "")) for h in headers]
        ws.append_row(row)

    def _find_row_index(self, ws, headers: List[str], key_col: str, value: str) -> Optional[int]:
        records = self._get_all(ws)
        try:
            idx = next(i for i, r in enumerate(records, start=2) if str(r.get(key_col)) == str(value))
            return idx
        except StopIteration:
            return None

    # Users
    def create_user(self, username: str, email: str, password_hash: str, avatar_url: str = "", bio: str = "") -> Dict[str, Any]:
        user_id = str(uuid.uuid4())
        rec = {
            "id": user_id,
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "avatar_url": avatar_url,
            "bio": bio,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._append(self.users_ws, ["id", "username", "email", "password_hash", "avatar_url", "bio", "created_at"], rec)
        return rec

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        for r in self._get_all(self.users_ws):
            if r.get("username") == username:
                return r
        return None

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        for r in self._get_all(self.users_ws):
            if str(r.get("id")) == str(user_id):
                return r
        return None

    # Posts
    def create_post(self, author_id: str, content: str, media_url: str, media_type: str, tags: str, description: str, subject: str) -> Dict[str, Any]:
        post_id = str(uuid.uuid4())
        rec = {
            "id": post_id,
            "author_id": author_id,
            "content": content,
            "media_url": media_url,
            "media_type": media_type,
            "tags": tags,
            "description": description,
            "subject": subject,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._append(self.posts_ws, ["id", "author_id", "content", "media_url", "media_type", "tags", "description", "subject", "created_at"], rec)
        return rec

    def list_posts(self, *, tag: str | None = None, q: str | None = None, subject: str | None = None, author_id: str | None = None) -> List[Dict[str, Any]]:
        posts = self._get_all(self.posts_ws)
        def matches(p):
            if author_id and str(p.get("author_id")) != str(author_id):
                return False
            if tag:
                tags = [t.strip().lower() for t in str(p.get("tags", "")).split(",") if t.strip()]
                if tag.lower() not in tags:
                    return False
            if subject and subject.lower() not in str(p.get("subject", "")).lower():
                return False
            if q:
                hay = (p.get("content", "") + " " + p.get("description", "")).lower()
                if q.lower() not in hay:
                    return False
            return True
        posts = [p for p in posts if matches(p)]
        posts.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return posts

    # Chats
    def get_or_create_chat(self, user1_id: str, user2_id: str) -> Dict[str, Any]:
        u1, u2 = sorted([user1_id, user2_id])
        for r in self._get_all(self.chats_ws):
            a, b = sorted([r.get("user1_id"), r.get("user2_id")])
            if a == u1 and b == u2:
                return r
        chat_id = str(uuid.uuid4())
        rec = {"id": chat_id, "user1_id": u1, "user2_id": u2, "created_at": datetime.utcnow().isoformat()}
        self._append(self.chats_ws, ["id", "user1_id", "user2_id", "created_at"], rec)
        return rec

    def list_chats_for_user(self, user_id: str) -> List[Dict[str, Any]]:
        out = []
        for r in self._get_all(self.chats_ws):
            if r.get("user1_id") == user_id or r.get("user2_id") == user_id:
                out.append(r)
        out.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return out

    def get_chat(self, chat_id: str) -> Optional[Dict[str, Any]]:
        for r in self._get_all(self.chats_ws):
            if r.get("id") == chat_id:
                return r
        return None

    def add_message(self, chat_id: str, sender_id: str, content: str) -> Dict[str, Any]:
        msg_id = str(uuid.uuid4())
        rec = {"id": msg_id, "chat_id": chat_id, "sender_id": sender_id, "content": content, "created_at": datetime.utcnow().isoformat()}
        self._append(self.messages_ws, ["id", "chat_id", "sender_id", "content", "created_at"], rec)
        return rec

    def list_messages(self, chat_id: str, since: str | None = None) -> List[Dict[str, Any]]:
        msgs = [m for m in self._get_all(self.messages_ws) if m.get("chat_id") == chat_id]
        if since:
            msgs = [m for m in msgs if m.get("created_at", "") > since]
        msgs.sort(key=lambda x: x.get("created_at", ""))
        return msgs

    # Chat read state
    def get_last_read_at(self, chat_id: str, user_id: str) -> Optional[str]:
        for r in self._get_all(self.chat_reads_ws):
            if r.get("chat_id") == chat_id and r.get("user_id") == user_id:
                return r.get("last_read_at")
        return None

    def set_last_read(self, chat_id: str, user_id: str, ts: Optional[str] = None) -> str:
        ts = ts or datetime.utcnow().isoformat()
        records = self._get_all(self.chat_reads_ws)
        # find row index by composite key
        for i, r in enumerate(records, start=2):
            if r.get("chat_id") == chat_id and r.get("user_id") == user_id:
                self.chat_reads_ws.update(f"D{i}", ts)
                return ts
        rec = {"id": str(uuid.uuid4()), "chat_id": chat_id, "user_id": user_id, "last_read_at": ts}
        self._append(self.chat_reads_ws, ["id", "chat_id", "user_id", "last_read_at"], rec)
        return ts

    def count_unread_chats_for_user(self, user_id: str) -> int:
        unread = 0
        chats = self.list_chats_for_user(user_id)
        all_msgs = self._get_all(self.messages_ws)
        for c in chats:
            cid = c.get("id")
            last_read = self.get_last_read_at(cid, user_id)
            # messages from others
            msgs = [m for m in all_msgs if m.get("chat_id") == cid and str(m.get("sender_id")) != str(user_id)]
            if not msgs:
                continue
            if not last_read:
                unread += 1
                continue
            latest_after = any((m.get("created_at", "") > last_read) for m in msgs)
            if latest_after:
                unread += 1
        return unread
