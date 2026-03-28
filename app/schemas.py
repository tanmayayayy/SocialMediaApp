from pydantic import BaseModel , EmailStr
from datetime import datetime
from typing import Literal, Optional
class Post(BaseModel):
    
    title: str
    content: str
    published: bool = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass



class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at:datetime


#using schemas for our response to the user (not showing unnecessary information like id and created_at fields etc)
class Post(PostBase): 
    id : int
    created_at:datetime
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode=True
     
class UserCreate(BaseModel):

    email : EmailStr #checks whether the entered email is valid or not 
    password: str

     



class UserLogin(BaseModel):
    email : EmailStr
    password : str


class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    user_id:Optional[int]=None


class Vote(BaseModel):
    post_id: int 
    dir : Literal[0,1]


class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode=True
