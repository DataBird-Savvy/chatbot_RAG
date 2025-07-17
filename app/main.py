from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime,timezone
from typing import List
import os
import requests
from dotenv import load_dotenv
import sys

from app.core.auth import authenticate_user, create_access_token, get_user
from app.db.db import SessionLocal
from app.db.models import User, ConversationHistory
from app.core.rag_pipeline import retrieve_context
from app.logger import logging
from app.exception import ChatBotException




load_dotenv()

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ---------- SCHEMAS ----------

class Token(BaseModel):
    access_token: str
    token_type: str

class UserOut(BaseModel):
    username: str

class Message(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    history: List[dict]

# ---------- UTILS ----------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- AUTH ENDPOINTS ----------

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        logging.info(f"Login attempt for user: {form_data.username}")
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            logging.warning(f"Login failed for user: {form_data.username}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        access_token = create_access_token(data={"sub": user.username})
        logging.info(f"Access token generated for user: {user.username}")
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(ChatBotException(e, sys))
        raise HTTPException(status_code=500, detail="Login failed due to server error")

@app.get("/users/me", response_model=UserOut)
async def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from jose import JWTError, jwt
    from app.core.auth import SECRET_KEY, ALGORITHM
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user(db, username=username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError as e:
        logging.error(ChatBotException(e, sys))
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logging.error(ChatBotException(e, sys))
        raise HTTPException(status_code=500, detail="Something went wrong")

# ---------- CHAT ENDPOINT ----------

@app.post("/chat", response_model=ChatResponse)
async def chat(
    msg: Message,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    from jose import JWTError, jwt
    from app.core.auth import SECRET_KEY, ALGORITHM

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user(db, username=username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        logging.info(f"User: {username} | Session: {msg.session_id} | Message: {msg.message}")

        # Store user message
        user_msg = ConversationHistory(
            user_id=user.id,
            session_id=msg.session_id,
            sender="user",
            message=msg.message,
            timestamp = datetime.now(timezone.utc)
        )
        db.add(user_msg)

        # Retrieve RAG context
        context_chunks = retrieve_context(msg.message,collection_name="support_collection")
        context_str = "\n".join(context_chunks)
        logging.info(f"Context retrieved for query: {context_chunks}")

        # LLM Call
        try:
            api_url = "https://api.us.inc/usf/v1/hiring/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "x-api-key": os.getenv("ULTRASAFE_API_KEY")
            }
            payload = {
                "model": "usf1-mini",
                "messages": [
                    {"role": "system", "content": f"Answer based only on the context below.\n\nContext:\n{context_str}"},
                    {"role": "user", "content": msg.message}
                ],
                "temperature": 0.7,
                "web_search": False,
                "stream": False,
                "max_tokens": 1000
            }
            api_response = requests.post(api_url, headers=headers, json=payload)
            response_data = api_response.json()
            response = response_data["choices"][0]["message"]["content"]
            logging.info("LLM response received successfully.")
        except Exception as e:
            logging.error(ChatBotException(e, sys))
            response = "Apologies, I couldn't generate a response right now."

        # Store bot response
        bot_msg = ConversationHistory(
            user_id=user.id,
            session_id=msg.session_id,
            sender="bot",
            message=response,
            timestamp = datetime.now(timezone.utc)
        )
        db.add(bot_msg)
        db.commit()

        # Return chat history
        history = db.query(ConversationHistory).filter_by(
            user_id=user.id, session_id=msg.session_id
        ).order_by(ConversationHistory.timestamp).all()

        chat_history = [
            {"sender": h.sender, "message": h.message, "timestamp": h.timestamp.isoformat()}
            for h in history
        ]

        return ChatResponse(response=response, history=chat_history)

    except Exception as e:
        logging.error(ChatBotException(e, sys))
        raise HTTPException(status_code=500, detail="Chat processing failed")
