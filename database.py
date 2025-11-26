import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Mock data for local fallback
LOCAL_DB_FILE = 'local_db.json'

class Database:
    def __init__(self):
        self.use_sheets = False
        self.client = None
        self.db = self._load_local_db()
        
        # Try to connect to Google Sheets
        if os.path.exists('credentials.json'):
            try:
                scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
                creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
                self.client = gspread.authorize(creds)
                self.use_sheets = True
                print("Connected to Google Sheets")
            except Exception as e:
                print(f"Google Sheets connection failed: {e}. Using local JSON.")
        else:
            print("No credentials.json found. Using local JSON database.")

    def _load_local_db(self):
        if os.path.exists(LOCAL_DB_FILE):
            with open(LOCAL_DB_FILE, 'r') as f:
                return json.load(f)
        return {"users": [], "posts": [], "messages": []}

    def _save_local_db(self):
        with open(LOCAL_DB_FILE, 'w') as f:
            json.dump(self.db, f, indent=4)

    def create_user(self, email, username, password):
        # In a real app, hash the password!
        user = {
            "id": len(self.db["users"]) + 1,
            "email": email,
            "username": username,
            "password": password, # Plaintext for prototype only
            "joined_at": str(datetime.now())
        }
        
        if self.use_sheets:
            # Implement Sheet logic here if needed
            pass
            
        self.db["users"].append(user)
        self._save_local_db()
        return user

    def get_user_by_email(self, email):
        for user in self.db["users"]:
            if user["email"] == email:
                return user
        return None

    def create_post(self, user_id, image_path, description, tags):
        post = {
            "id": len(self.db["posts"]) + 1,
            "user_id": user_id,
            "image_path": image_path,
            "description": description,
            "tags": tags, # List of strings
            "created_at": str(datetime.now())
        }
        self.db["posts"].append(post)
        self._save_local_db()
        return post

    def get_all_posts(self):
        return self.db["posts"]

    def get_user_posts(self, user_id):
        return [p for p in self.db["posts"] if p["user_id"] == user_id]

    def add_message(self, sender_id, content):
        msg = {
            "id": len(self.db["messages"]) + 1,
            "sender_id": sender_id,
            "content": content,
            "timestamp": str(datetime.now())
        }
        self.db["messages"].append(msg)
        self._save_local_db()
        return msg

    def get_messages(self):
        return self.db["messages"]

db = Database()
