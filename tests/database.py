from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
import pytest


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:    @{settings.database_hostname}/{settings.database_name}_test'

 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autoflush=False,bind=engine)

Base.metadata.create_all(bind=engine)


#Dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()   

app.dependency_overrides[get_db] = override_get_db 


# client = TestClient(app)

@pytest.fixture(scope="module")
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    #run our code before we run our test
    yield  TestClient(app)
    # run our code after our test finished