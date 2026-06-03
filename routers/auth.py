# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from starlette import status

from database import users_db, db_ids
from schemas import UserCreate, TokenResponse
from security import get_password_hash, verify_password, create_access_token

# Initialize the router and add a tag for Swagger UI organization
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    # Check if username is already taken
    for user in users_db:
        if user["username"].casefold() == user_data.username.casefold():
            raise HTTPException(status_code=400, detail="Username already exists")
    
    # Hash password and save
    hashed_pw = get_password_hash(user_data.password)
    new_user = {
        "id": db_ids.get_new_user_id(),
        "username": user_data.username,
        "hashed_password": hashed_pw
    }
    users_db.append(new_user)
    
    return {"message": "User created successfully"}

@router.post("/login", response_model=TokenResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # 1. Find the user
    target_user = None
    for user in users_db:
        if user["username"].casefold() == form_data.username.casefold():
            target_user = user
            break
            
    # 2. Verify existence and password match
    if not target_user or not verify_password(form_data.password, target_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
        
    # 3. Generate and return the JWT
    token = create_access_token(username=target_user["username"], user_id=target_user["id"])
    return {"access_token": token, "token_type": "bearer"}