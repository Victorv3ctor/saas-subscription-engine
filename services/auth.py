from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from exceptions.user import WrongCredentials
from services.user_service import user_query_by_id, user_query_by_username
from services.security import security_check_pwd

load_dotenv()
secret_key = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
security = HTTPBearer()



def check_user_credentials(data_username, data_pwd):
    user = user_query_by_username(data_username)
    if not security_check_pwd(data_pwd, user.pwd):
        raise WrongCredentials()
    return user

def login_in(data_username, data_pwd):
    user = check_user_credentials(data_username, data_pwd)
    token = create_token(user.user_id)
    return token

def decode_token(token):
    try:
        return jwt.decode(token, secret_key, algorithms=[ALGORITHM])
    except JWTError as e:
        raise ValueError(str(e))

def create_token(user_id):
    payload = {
        "sub" : str(user_id),
        "exp" : datetime.now() + timedelta(minutes=60)
    }
    return jwt.encode(payload, secret_key, ALGORITHM)

def get_current_account(
        credentials: HTTPAuthorizationCredentials=Depends(security),
):
    token = credentials.credentials
    payload = decode_token(token)
    user_id = int(payload.get('sub'))
    user = user_query_by_id(user_id) #dodac conn
    return user




