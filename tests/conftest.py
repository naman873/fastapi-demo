from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
import pytest
from app import models
from app.oauth2 import create_access_token
from fastapi import Depends


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:    @{settings.database_hostname}/{settings.database_name}_test'

 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autoflush=False,bind=engine)

Base.metadata.create_all(bind=engine)


#Dependency
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()   




# client = TestClient(app)


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()  
    
@pytest.fixture(scope="function")
def client(session):    

    def override_get_db():
        try:
            yield session
        finally:
            session.close()   
    app.dependency_overrides[get_db] = override_get_db 
    yield  TestClient(app)
    

@pytest.fixture
def test_users(client):
    user_data = {"email":"naman12345@gmail.com","password":"12345"}
    
    res = client.post("/users/",json= user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password']= user_data["password"]
    return new_user    


@pytest.fixture
def test_users2(client):
    user_data = {"email":"naman123456@gmail.com","password":"12345"}
    
    res = client.post("/users/",json= user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password']= user_data["password"]
    return new_user    


@pytest.fixture
def token(test_users):
    return create_access_token({"user_id":test_users["id"]})


@pytest.fixture
def authorized_client(client,token):
    client.headers = {
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_post(test_users,session,test_users2):
    posts_data = [{"title":"first title","content":"content","owner_id":test_users["id"]},
                  {"title":"second title","content":"content","owner_id":test_users["id"]},
                  {"title":"third title","content":"content","owner_id":test_users["id"]},
                  {"title":"fourth title","content":"content","owner_id":test_users2["id"]},
                  ]
    

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)

    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()

    return posts