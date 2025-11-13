# CleanChem Social (Flask)

A small social network built with Flask + Tailwind that runs locally, featuring:

- Multilingual (pt-br/en/es)
- Gallery with local uploads (images/videos) and filters (tags, description, subject)
- User registration/login (Flask-Login)
- User pages listing only that author’s posts
- User-to-user chats (AJAX polling)
- AI Chat using OpenAI
- Google Sheets as the database

## Requirements

- Python 3.10+
- A Google Cloud Service Account with access to a Google Sheet
- OpenAI API key for AI chat

## Setup

1) Clone and enter the project folder, then install deps:

```
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2) Google Sheets credentials:

- Create a Service Account in Google Cloud and download the JSON key file.
- Share your target Spreadsheet with the service account email (Editor).
- Set one of the following:
  - `GOOGLE_APPLICATION_CREDENTIALS` to the JSON file path; or
  - `GOOGLE_SHEETS_CREDS_JSON` with the file contents.
- Provide spreadsheet reference:
  - Prefer `GOOGLE_SHEETS_SPREADSHEET_ID` (Spreadsheet ID), or
  - `GOOGLE_SHEETS_SPREADSHEET_NAME` (defaults to "CleanChem Social").

Create the spreadsheet manually and leave it empty. The app will create the worksheets it needs: `users`, `posts`, `chats`, `messages`.

3) OpenAI API key:

Set `OPENAI_API_KEY` in your environment.

4) Run

```
set SECRET_KEY=dev-secret
set OPENAI_API_KEY=sk-...
set GOOGLE_APPLICATION_CREDENTIALS=C:\\path\\to\\service_account.json
set GOOGLE_SHEETS_SPREADSHEET_ID=your_sheet_id
python app.py
```

Then open http://127.0.0.1:5000

## Notes

- Uploads are saved under `uploads/` in the project directory and served via `/uploads/<file>`.
- Allowed extensions: png, jpg, jpeg, gif, mp4, mov, webm (change via `ALLOWED_EXTENSIONS`).
- Language can be changed using the selector in the navbar; it stores preference in the session.
- User chat uses simple polling every 2 seconds; it’s adequate for local testing without WebSockets.
- For first use, register two users, start a chat with the second user’s username, and exchange messages.

## Troubleshooting

- If you see `Google Sheets credentials not configured`, set the environment variables as described above and ensure the spreadsheet is shared with the service account.
- If AI chat returns an error, verify `OPENAI_API_KEY` and network access.
- On Windows, ensure the virtualenv is activated before running.

## Color Palette

- #FFFFFF, #F3F3F3, #FBD64A, #2C2E43

