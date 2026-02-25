from jose import JWTError,jwt
from datetime import datetime, timedelta, timezone
# from app.schemas import schemas
from . import schemas, database,models

from  fastapi import Depends,status, HTTPException
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login') # this is our login endpoint (without the backslash)

#it tells fastapi that the users should get token from /login URL 

#depends(oauth2_scheme) extracts the token automatically 




#secret key
#algorithm
#expiration time of token 

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data:dict):
    to_encode=data.copy()

    expire=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM) #creating the jwt token 
    
    return encoded_jwt


def verify_access_token(token:str,credentials_exception):


        
    try:
            
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        
        # print("JWT PAYLOAD:", payload)


        user_id=payload.get("user_id")

        if user_id is None:
            raise credentials_exception
    
        token_data = schemas.TokenData(user_id=user_id)

    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credentials_exception =  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate credentials',headers={"WWW-Authenticate":"Bearer"})

    TOKEN = verify_access_token(token,credentials_exception)

    user = db.query(models.User).filter(models.User.id==TOKEN.user_id).first()

    if user is None:
        raise credentials_exception
    print(TOKEN)
    print(type(TOKEN))

    return user

