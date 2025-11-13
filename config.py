import os


class Config:
    def __init__(self):
        # Flask
        self.SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

        # Uploads
        self.UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", os.path.join(os.getcwd(), "uploads"))
        self.ALLOWED_EXTENSIONS = set((os.getenv("ALLOWED_EXTENSIONS", "png,jpg,jpeg,gif,mp4,mov,webm").split(",")))

        # Google Sheets
        # Prefer spreadsheet ID for reliability; falls back to name
        self.GOOGLE_SHEETS_SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
        self.GOOGLE_SHEETS_SPREADSHEET_NAME = os.getenv("GOOGLE_SHEETS_SPREADSHEET_NAME", "CleanChem Social")
        self.GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.GOOGLE_SHEETS_CREDS_JSON = os.getenv("GOOGLE_SHEETS_CREDS_JSON")

        # OpenAI
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        # i18n
        self.LANGUAGES = [lang.strip() for lang in os.getenv("LANGUAGES", "pt-br,en,es").split(",")]
        self.DEFAULT_LANG = os.getenv("DEFAULT_LANG", "pt-br")

