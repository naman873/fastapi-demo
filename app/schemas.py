from pydantic import BaseModel,ConfigDict,EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id:int
    owner: UserOut

    # we are using this because pydantic's orm_mode will tell pydantic model to read the data even if it not a dict, but an orm model
    class Config():
        # ConfigDict(from_attributes=True)
        # orm_mode = True
        model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config():
        model_config = ConfigDict(from_attributes=True)

class UsesCreate(BaseModel):
    email:EmailStr
    password:str


class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime



class UserLogin(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token:str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None     



class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)