from dataclasses import dataclass
from flask_login import UserMixin


@dataclass
class User(UserMixin):
    id: str
    username: str
    email: str | None = None
    avatar_url: str | None = None

    def get_id(self):
        return self.id

    @staticmethod
    def from_record(rec: dict) -> "User":
        return User(
            id=str(rec.get("id")),
            username=rec.get("username"),
            email=rec.get("email"),
            avatar_url=rec.get("avatar_url"),
        )

