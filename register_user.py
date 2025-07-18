from sqlalchemy.orm import Session
from chatapp.db.db import SessionLocal
from chatapp.db.models import User
from chatapp.core.auth import hash_password

def register_user(username: str, password: str):
    db: Session = SessionLocal()

    # Check if user already exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        print("❌ User already exists.")
        return

    # Hash and store user
    hashed_pwd = hash_password(password)
    new_user = User(username=username, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print(f"✅ User '{username}' registered.")

if __name__ == "__main__":
    username = input("Username: ")
    password = input("Password: ")
    register_user(username, password)
