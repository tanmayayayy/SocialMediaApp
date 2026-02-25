from fastapi import FastAPI,Response,status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel 
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()
class Post(BaseModel):
    postid: int
    title: str
    content: str
    published: bool



while True:
    print("CONNECTING TO DATABASE")
    try: 
        conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password="Lap82@tanc",cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("DataBase Connected") 
        break

    except Exception as e:
        print('Connecting to database failed \n')
        print("The error was" , e)
        time.sleep(2)


my_posts=[{"title": "title of post 1 ", "content":"content of post 1 ", "postid":1},{"title":"favourite foods", "content":"butter chicken recipe","postid":2} ]

# a=["tan","rid","raghav","khushaal"]


def find_post(postid:int):
    for p in my_posts:
        if p["postid"] == postid:
            return p
        



@app.get("/posts")
def getposts():
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()
    print(posts)
    return {"data":posts}

# @app.get("/")
# async def root():
#     return a[0]


# @app.get("/rid")
# async def root():
#     return a[1]


# @app.get("/raghav")
# async def root():
#     return a[2]


# @app.get("/khushaal")
# async def root():
#     return a[3]

# @app.post("/createposts")
# async def create_posts(payLoad:dict=Body(...)):
#     print(payLoad)
#     return {"1":f"Data of first post is {payLoad['first']}"}

# @app.post("/createposts")
# async def create_posts(new_post:Post):
#     print(new_post)
#     return {f"title of the {new_post.postid} post is {new_post.title}"}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_posts(new_post:Post):
   
    cursor.execute(""" insert into posts(title,content,published) values (%s,%s,%s) RETURNING * """,(new_post.title,new_post.content,new_post.published))

    new_post=cursor.fetchone()
    conn.commit()  
    return {"data":new_post }

# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# async def create_posts(new_post:Post):
   
#     new_post_dict=new_post.model_dump()
#     new_post_dict['postid']=randrange(0,10000000)
#     my_posts.append(new_post_dict)
#     print(my_posts)
#     return {"data":my_posts }

@app.get("/posts/{postid}")

def get_post(postid:int,response:Response):
    cursor.execute(""" select * from posts where postid = %s""", str(postid))
    post=cursor.fetchone()
    
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ERROR 404 NOT FOUND")
        
    return {"post_detail":post}


# @app.get("/posts/{postid}")

# def get_post(postid:int,response:Response):
#     post=find_post(postid)
#     # if not post:
#     #     response.status_code=404

#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ERROR 404 NOT FOUND")
#         # response.status_code=status.HTTP_404_NOT_FOUND
#         # return "NOT FOUND"
#     return {"post_detail":post}

@app.delete("/posts/{postid}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(postid:int):
    cursor.execute("""delete from posts where postid = %s RETURNING * """,(postid,))
    deleted_post=cursor.fetchone()
    conn.commit()
            
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return {Response(status_code=status.HTTP_204_NO_CONTENT)}
# @app.delete("/posts/{postid}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(postid:int):
#     for i,p in enumerate(my_posts):
#         if p['postid']==postid:

#             my_posts.pop(i)
#             return {"deleted successfully":Response(status_code=status.HTTP_204_NO_CONTENT)}
#             break
        
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    

@app.put("/posts/{postid}")
def update_post(postid:int,post:Post):
            
        cursor.execute(""" update posts set title=%s,content=%s,published=%s where postid=%s RETURNING * """,(post.title,post.content,post.published,postid))
        updated_post=cursor.fetchone()
        conn.commit()

        if updated_post is None:    
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        else:
            return "post updated"
    
# def update_post(postid:int,post:Post):
#     for p in my_posts:
#         if p['postid'] == postid:

#             p['title']=post.title
#             p['rating']=post.rating
#             p['content']=post.content
#             p['postid']=post.postid
#             return "post updated"
        
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    

