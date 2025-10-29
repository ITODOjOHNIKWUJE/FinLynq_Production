from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Dict
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "replace_this_with_a_strong_secret_in_prod"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI(title="FinLynq API (Minimal)")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
USERS: Dict[str, Dict] = {}

class RegisterIn(BaseModel):
    phone: str
    password: str

@app.post("/auth/register")
async def register(payload: RegisterIn):
    if payload.phone in USERS:
        raise HTTPException(status_code=400, detail="User exists")
    USERS[payload.phone] = {"password": payload.password, "balance": 0.0, "kyc_status": "none"}
    return {"msg": "registered", "phone": payload.phone}

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/auth/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = USERS.get(form_data.username)
    if not user or user.get("password") != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = USERS.get(username)
    if user is None:
        raise credentials_exception
    return username

@app.get("/wallet/balance")
async def wallet_balance(phone: str = None, current_user: str = Depends(get_current_user)):
    if phone is None:
        phone = current_user
    if phone != current_user:
        raise HTTPException(status_code=403, detail="Forbidden")
    user = USERS.get(phone)
    return {"phone": phone, "balance": user.get("balance", 0.0)}

@app.post("/wallet/deposit")
async def wallet_deposit(amount: float, current_user: str = Depends(get_current_user)):
    user = USERS.get(current_user)
    user["balance"] += float(amount)
    return {"status": "ok", "balance": user["balance"]}
import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

