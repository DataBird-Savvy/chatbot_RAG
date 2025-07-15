# register_user.py


from app.db.db import SessionLocal
from app.db.models import User
from app.core.auth import hash_password


def create_user(username: str, password: str):
    db = SessionLocal()
    hashed_pw = hash_password(password)
    new_user = User(username=username, hashed_password=hashed_pw)

    db.add(new_user)
    db.commit()
    db.close()
    print(f" User '{username}' created successfully.")

if __name__ == "__main__":
    create_user("jiyamary", "mypassword")
