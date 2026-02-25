from fastapi import FastAPI,Response,status, HTTPException,Depends,APIRouter
from app import models, oauth2,schemas,utils, oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router=APIRouter(
    tags=['Authentication']
)

@router.post("/login",response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session = Depends(get_db)):


#oauth2 return type is as follows, whatever the user write (email or username) will be stored in variable named username and the password in the variable password

#{"username": "sldkfjasdf", 
#"password":"asdfjkl;"}

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid email')
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid Password')
 
    #create a token
    #return token 


    access_token=oauth2.create_access_token(data={"user_id":user.id}) #this is the data that we want to put in the payload

    
    return {
    "access_token": access_token,
    "token_type": "bearer"
}
