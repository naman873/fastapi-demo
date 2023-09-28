from app import schemas
import pytest

def test_get_all_posts(authorized_client,test_post):
    res = authorized_client.get("/posts/")


    def validate(post):
        return schemas.PostOut(**post)

    posts_map = map(validate,res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_post)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client,test_post):
    res = client.get("/posts/")
    assert res.status_code == 401





def test_unauthorized_user_get_one_posts(client,test_post):
    res = client.get(f"/posts/{test_post[0].id}")
    assert res.status_code == 401



def test_get_one_post_not_exist(authorized_client,test_post):
    res = authorized_client.get(f"/posts/100")
    assert res.status_code == 404


def test_get_one_post(authorized_client,test_post):
    res = authorized_client.get(f"/posts/{test_post[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_post[0].id


@pytest.mark.parametrize("title,content,published",[
    ("awesome new title","awesome new content",True),
    ("fav pizza","Cheese Pizza",True),
    ("fav show","friends",True),
])
def test_create_post(authorized_client,test_users,test_post,title,content,published):
    res = authorized_client.post("/posts/",json={"title":title,"content":content,"pubished":published})
    created_post  = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_users["id"]



def test_create_post_default_published_true(authorized_client,test_users,test_post):
    res = authorized_client.post("/posts/",json={"title":"title","content":"content"})
    created_post  = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == "title"
    assert created_post.content == "content"
    assert created_post.published == True 
    assert created_post.owner_id == test_users["id"]




def test_anauthorized_user_create_post(client,test_post):
    res = client.post("/posts/",json={"title":"title","content":"content"})
    assert res.status_code == 401  



def test_unauthorized_user_delete_post(client,test_users,test_post):
    res = client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 401  



def test_delete_post(authorized_client,test_users,test_post):
    res = authorized_client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client,test_users,test_post):
    res = authorized_client.delete("/posts/435")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client,test_users,test_post):
    res = authorized_client.delete(f"/posts/{test_post[3].id}")
    assert res.status_code == 403    


def test_update_post(authorized_client,test_users,test_post):
    data = {"title":"updated title","content":"content","id":test_post[0].id}

    res = authorized_client.put(f"/posts/{test_post[0].id}",json=data)
    updated_post =  schemas.Post(**res.json())
    assert res.status_code == 201
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client,test_users,test_users2,test_post):
        data = {"title":"updated title","content":"content","id":test_post[3].id}

        res = authorized_client.put(f"/posts/{test_post[3].id}",json=data)
        
        assert res.status_code == 403


def test_unauthorized_user_update_post(client,test_users,test_post):
    res = client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 401  


def test_update_post_non_exist(authorized_client,test_users,test_post):
    data = {"title":"updated title","content":"content","id":test_post[3].id}
    res = authorized_client.put("/posts/435",json= data)
    assert res.status_code == 404    