# routers/transactions.py
from fastapi import APIRouter, HTTPException, Path, Query
from starlette import status
from typing import Optional, Literal

from database import transactions_db, db_ids
from schemas import TransactionCreate
from dependencies import user_dependency

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# 1. CREATE TRANSACTION
@router.post("/", status_code=status.HTTP_201_CREATED)
async def log_transaction(transaction_data: TransactionCreate, user: user_dependency):
    new_txn = {
        "id": db_ids.get_new_transaction_id(),
        "amount": transaction_data.amount,
        "category": transaction_data.category,
        "transaction_type": transaction_data.transaction_type,
        "description": transaction_data.description,
        "user_id": user["id"] # Securely link the transaction to the logged-in user
    }
    transactions_db.append(new_txn)
    return {"message": "Transaction logged successfully", "id": new_txn["id"]}

# 2. READ TRANSACTIONS (With Optional Query Parameter)
@router.get("/", status_code=status.HTTP_200_OK)
async def get_my_transactions(
    user: user_dependency, 
    # Query param to filter. None means show all.
    type_filter: Optional[Literal["income", "expense"]] = Query(default=None) 
):
    # First, only get transactions belonging to THIS user
    user_txns = [t for t in transactions_db if t["user_id"] == user["id"]]
    
    # Then, apply the query filter if the user provided one in the URL
    if type_filter:
        user_txns = [t for t in user_txns if t["transaction_type"] == type_filter]
        
    return user_txns

# 3. UPDATE TRANSACTION
@router.put("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_transaction(
    user: user_dependency, 
    transaction_data: TransactionCreate,
    transaction_id: int = Path(gt=0)
):
    for i in range(len(transactions_db)):
        if transactions_db[i]["id"] == transaction_id:
            # Check ownership
            if transactions_db[i]["user_id"] != user["id"]:
                raise HTTPException(status_code=403, detail="Not authorized to edit this")
            
            # Update data
            transactions_db[i]["amount"] = transaction_data.amount
            transactions_db[i]["category"] = transaction_data.category
            transactions_db[i]["transaction_type"] = transaction_data.transaction_type
            transactions_db[i]["description"] = transaction_data.description
            return
            
    raise HTTPException(status_code=404, detail="Transaction not found")

# 4. DELETE TRANSACTION
@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(user: user_dependency, transaction_id: int = Path(gt=0)):
    for i in range(len(transactions_db)):
        if transactions_db[i]["id"] == transaction_id:
            # Check ownership
            if transactions_db[i]["user_id"] != user["id"]:
                raise HTTPException(status_code=403, detail="Not authorized to delete this")
            
            transactions_db.pop(i)
            return
            
    raise HTTPException(status_code=404, detail="Transaction not found")