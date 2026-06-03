# security.py
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

# 1. Password Hashing Configuration
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)

# 2. JWT Configuration
# Note: In a real app, load this SECRET_KEY from a hidden .env file!
SECRET_KEY = "my_super_secret_master_key_for_finance_api"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(username: str, user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # The payload (claims) encoded into the token
    payload = {
        "sub": username,
        "id": user_id,
        "exp": expire
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)