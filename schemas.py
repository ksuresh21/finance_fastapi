# schemas.py
from pydantic import BaseModel, Field
from typing import Literal, Optional

# --- AUTHENTICATION SCHEMAS ---
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=5, description="User's plain text password")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# --- TRANSACTION SCHEMAS ---
class TransactionCreate(BaseModel):
    # Enforce amount must be greater than 0
    amount: float = Field(gt=0, description="Amount must be greater than zero")
    category: str = Field(min_length=2, max_length=50, description="e.g., Groceries, Salary, Rent")
    
    # Literal enforces that the user MUST type exactly one of these two strings
    transaction_type: Literal["income", "expense"]
    
    # Optional field that defaults to None if the user doesn't provide it
    description: Optional[str] = Field(default=None, max_length=255)

class TransactionResponse(BaseModel):
    id: int
    amount: float
    category: str
    transaction_type: str
    description: Optional[str]
    user_id: int