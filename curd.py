from typing import Dict, Optional

from pydantic import BaseModel

# Sample user model
class User(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

# In-memory user database
fake_users_db: Dict[str, User] = {}

# CRUD operations

def get_user(username: str) -> Optional[User]:
    return fake_users_db.get(username)

def create_user(user: User) -> User:
    if user.username in fake_users_db:
        raise ValueError("User already exists")
    fake_users_db[user.username] = user
    return user

def update_user(username: str, user_data: dict) -> User:
    if username not in fake_users_db:
        raise ValueError("User not found")
    user = User(**user_data)
    fake_users_db[username] = user
    return user

def delete_user(username: str) -> None:
    if username not in fake_users_db:
        raise ValueError("User not found")
    del fake_users_db[username]
