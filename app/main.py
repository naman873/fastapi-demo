from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post,user,auth,vote
from .config import settings

  
models.Base.metadata.create_all(bind=engine)

app  = FastAPI()

origins = ["https://www.google.com"]
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# we are not using this postgres library to run raw sql we are now using sqlalchemy
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='    ',cursor_factory=RealDictCursor)
#         cursor =  conn.cursor()
#         print("database connection was succesfull")
#         break
#     except Exception as error:
#         print("Connecting to database fail.")
#         print("Error ",error)  
#         time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message":"Hello World"}




