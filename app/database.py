import time

import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

from urllib.parse import quote_plus #to convert special characters in password to special format to avoid conflicts

password = quote_plus(settings.database_password)

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


Base=declarative_base() #defining a base class


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()



# while True:
#     print("CONNECTING TO DATABASE")
#     try: 
#         conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password="Lap82@tanc",cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("DataBase Connected") 
#         break

#     except Exception as e:
#         print('Connecting to database failed \n')
#         print("The error was" , e)
#         time.sleep(2)


