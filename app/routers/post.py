from .. import models,schemas,oauth2
from fastapi import  Response,status, HTTPException,Depends, APIRouter
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import  func
from ..database import get_db
from typing import List


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


my_posts = [{"title":"this is 1 title","content":"this is a content","id":1},{"title":"this is 2 title","content":"this is a content","id":2}]


# @router.get("/",response_model=List[schemas.Post])
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit: int =10,skip:int=0,search:Optional[str]=""):
    # cursor.execute(""" select * from posts """)
    # posts = cursor.fetchall()

    #sqlalchemy
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    result_post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
   
   
    return result_post


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
   
    # post_dict = post.model_dump()
    # post_dict["id"] = randrange(0,100000000)
    # my_posts.append(post_dict)


    # This command can be attacked by sql injecton dont use like this. 
    # cursor.execute(f""" insert into posts (title,content,published) values ({post.title},{post.content},{post.published}) """,)

    # cursor.execute(""" insert into posts (title,content,published) values (%s,%s,%s) returning *""",(post.title,post.content,post.published))
    # new_post= cursor.fetchone()
    # conn.commit()
  
    #sqlalchemy
    # print(current_user.email)
    # new_post=models.Post(title=post.title,content=post.content,published= post.published)
    #or
    new_post=models.Post(owner_id=current_user.id,**post.model_dump()) 
    db.add(new_post)
    db.commit()
    # next line saves the latest post in the values new_post
    db.refresh(new_post)

    return new_post 
  

# @router.get("/{id}",response_model=schemas.Post) 
@router.get("/{id}",response_model=schemas.PostOut) 
def get_post(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    # post = find_post(id)

    # cursor.execute(""" select * from posts where id = %s """,(str(id),)) 
    # post = cursor.fetchone()

    #sqlalchemy
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"post with id: {id} was not found"}
        # or
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")   
    return post    


def find_post(id):
    for post in my_posts:
        if(post["id"]==int(id)):  
            return post
        
 
def find_post_index(id):
    for i,p in enumerate(my_posts):
        if(p["id"]==int(id)):
            return i      

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    # post = find_post(id)

    # cursor.execute(""" delete from posts where id = %s returning * """,(str(id),))
    # post = cursor.fetchone()
    # conn.commit()

    #sqlalchemy
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found.")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not Authorize to perform reqested action")

    # my_posts.remove(post)

    post.delete(synchronize_session=False)
    db.commit()
   
    return Response(status_code= status.HTTP_204_NO_CONTENT)


@router.put("/{id}",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def update_post(nPost:schemas.PostCreate,id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    # index = find_post_index(id)

 
    # cursor.execute(""" update posts set title = %s, content = %s, published = %s where id = %s returning *""", (nPost.title,nPost.content,nPost.published,str(id),))
    # post = cursor.fetchone() 
    # conn.commit()
  
    #sqlalchemy

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not Authorize to perform reqested action")
     

    post_query.update(nPost.model_dump(),synchronize_session=False) 
    db.commit()
  
    # post_dict = nPost.model_dump()
    # post_dict["id"] = int(id)
    # my_posts[index] = post_dict

    return post_query.first()   