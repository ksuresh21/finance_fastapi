# dependencies.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Annotated
from security import SECRET_KEY, ALGORITHM

# Tells FastAPI the endpoint where users go to get their token.
# This powers the Swagger UI "Authorize" lock button.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# This function runs before any protected endpoint
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
            
        # Return the extracted user data as a dictionary
        return {"username": username, "id": user_id}
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# We create the dependency variable here to be injected into our routers
user_dependency = Annotated[dict, Depends(get_current_user)]