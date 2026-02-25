
from fastapi import FastAPI,Response,status, HTTPException,Depends,APIRouter
from app import models,schemas,utils,database,mainsql
from app.database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas import PostCreate
from app import oauth2 


router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#because all the path operations in this file start from /posts we can add a prefix instead of writing it again and again on each operation



@router.get("/",response_model=List[schemas.Post])
def getposts(db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user), Limit:int=10,skip:int = 0,search:Optional[str] =""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts=cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    return posts



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
async def create_posts(post:PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
   
    # new_post = models.Post(title=post.title,content=post.content,published=post.published)
    print(current_user)

    print(current_user.email)
    new_post=models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #acts like RETURNING * because it refreshes
    return new_post



@router.get("/{postid}",response_model=schemas.Post)

def get_post(postid:int,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id == postid).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ERROR 404 NOT FOUND")
        
    return post


@router.delete("/{postid}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(postid:int, db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id == postid).first()
    
            
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="NOT AUTHORIZED TO PERFORM REQUESTED ACTION")
    else:
        db.query(models.Post).filter(models.Post.id == postid).delete(synchronize_session=False)
        db.commit()
        return {Response(status_code=status.HTTP_204_NO_CONTENT)}
   

@router.put("/{postid}",response_model=schemas.Post)
def update_post(postid:int,post:PostCreate,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
            
        post_query=db.query(models.Post).filter(models.Post.id == postid)
        updated_post=post_query.first()
        if updated_post is None:    
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if post.owner_id!=current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="NOT AUTHORIZED TO PERFORM REQUESTED ACTION")
             
        else:
            post_query.update(post.model_dump(),synchronize_session=False)
            db.commit()
            db.refresh(updated_post)
            return updated_post
     