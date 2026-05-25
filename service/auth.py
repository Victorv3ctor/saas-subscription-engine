#LIBRARIES
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

#REPOSITORY
from repository.repository import Repository

#DEPENDENCIES
from dependencies.get_repo import get_repo

#LOADS
load_dotenv()
secret_key = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
security = HTTPBearer()

def create_token(user_id): #service AUTH
    payload = {
        "sub" : str(user_id),
        "exp" : datetime.now() + timedelta(minutes=60)
    }
    return jwt.encode(payload, secret_key, ALGORITHM)

def decode_token(token): #service AUTH
    try:
        return jwt.decode(token, secret_key, algorithms=[ALGORITHM])
    except JWTError as e:
        raise ValueError(str(e))

def get_current_account(
        credentials: HTTPAuthorizationCredentials=Depends(security),
        repo: Repository = Depends(get_repo),
):
    token = credentials.credentials
    payload = decode_token(token)
    user_id = int(payload.get('sub'))
    user = repo.get_user_by_id(user_id)
    return user