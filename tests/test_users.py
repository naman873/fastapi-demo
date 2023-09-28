from app import schemas
import pytest
from jose import jwt
from app.config import settings


# def test_root(client):
#     res = client.get("/")
#     print(res.json().get("message"))
#     assert res.json().get("message") == "Hello World"
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/",json={"email":"naman1234@gmail.com","password":"12345"})  
     
    new_user = schemas.UserOut(**res.json())

    assert new_user.email == "naman1234@gmail.com"
    assert res.status_code == 201


def test_login_user(client,test_users):
    res = client.post("/login",data={"username":test_users['email'],"password":test_users['password']})  
    
    login_res = schemas.Token(**res.json( ))
    payload = jwt.decode(login_res.access_token,settings.secret_key,algorithms=[settings.algorithm])
 
    id = payload.get("user_id")

    assert id == test_users['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200 


@pytest.mark.parametrize("email, password, status_code",[("wrongemail@gmai.com",'password1234',403),("sanjeev@gmai.com","wrongpassword",403),(None,"passworfd123",422)])
def test_incorret_login(test_users,client,email,password,status_code):
    res = client.post("/login", data={"username":email,"password":password})

    assert res.status_code == status_code


