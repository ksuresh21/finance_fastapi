# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import our modular routers
from routers import auth, transactions

app = FastAPI(
    title="Personal Finance Tracker API",
    description="A complete API for managing personal income and expenses with JWT Authentication.",
    version="1.0.0"
)

# --- CORS CONFIGURATION ---
# Necessary if you ever build a React, Vue, or HTML frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# --- INCLUDE ROUTERS ---
app.include_router(auth.router)
app.include_router(transactions.router)

@app.get("/", tags=["Health Check"])
async def root():
    return {"status": "Finance Tracker API is running securely!"}