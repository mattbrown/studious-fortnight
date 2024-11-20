import pytest
from microblog import create_app, db
from microblog.models import User, Post
import uuid

@pytest.fixture
def app():
    test_config = {
        "SQLALCHEMY_DATABASE_URI": "postgresql://admin:root@localhost:5432/test"
    }

    app = create_app(test_config)
    yield app


@pytest.fixture
def client(app):
    yield app.test_client()


@pytest.fixture(autouse=True)
def db_setup(app):
    with app.app_context():
        db.drop_all()
        db.create_all()


@pytest.fixture
def user_for_test(app):
    with app.app_context():
        test_user = User(name="test_get_guy", email="test@example.com")
        db.session.add(test_user)
        db.session.commit()
        yield test_user

@pytest.fixture
def post_for_test(app, user_for_test):
    with app.app_context():
        test_post = Post(
            title='a new blog',
            content = 'hello everyone I have decided to write a bunch and make you read it',
            user_id = user_for_test.id
        )
        db.session.add(test_post)
        db.session.commit()
        yield test_post


def test_get_all_posts(app, client, user_for_test, post_for_test):
    response = client.get('/posts')
    assert response.status_code == 200
    json_response = response.get_json()
    assert len(json_response) == 1
    assert json_response[0]['title'] == post_for_test.title
    assert json_response[0]['content'] == post_for_test.content


def test_add_new_post(app, client, user_for_test):
    post_json = {
        'title': 'a second blog entry?',
        'content': 'guys look how productive I am',
        'user_id': str(user_for_test.id)
    }
    response = client.post('/posts', json=post_json)
    assert response.status_code == 200

def test_post_no_user(app, client):
    post_json = {
        'title': 'anonymous blog entry',
        'content': 'I am not a real user',
        'user_id': str(uuid.uuid4())
    }
    response = client.post('/posts', json=post_json)
    assert response.status_code == 400

def test_get_post_by_id(app, client, user_for_test, post_for_test):
    response = client.get(f'/posts/{post_for_test.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == post_for_test.title
    assert data['content'] == post_for_test.content

def test_get_post_does_not_exist(app, client):
    response = client.get(f'/posts/{uuid.uuid4()}')
    assert response.status_code == 404

def test_update_post(app, client, user_for_test, post_for_test):
    update_data = post_for_test.to_dict()
    update_data['title'] = 'I changed my mind on title'
    update_data['content'] = 'and I want to rewrite this whole post'

    response = client.put(f'/posts/{post_for_test.id}', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == update_data['title']
    assert data['content'] == update_data['content']

def test_update_post_not_found(app, client):
    test_post = {
        'title': 'a bad egg',
        'content': 'does this even exist?'
    }
    response = client.put(f'/posts/{uuid.uuid4()}')
    assert response.status_code == 404

def test_update_user_not_found(app, client, user_for_test, post_for_test):
    update_data = post_for_test.to_dict()
    update_data['title'] = 'I changed my mind on title'
    update_data['content'] = 'and I want to rewrite this whole post'
    update_data['user_id'] = str(uuid.uuid4())

    response = client.put(f'/posts/{post_for_test.id}', json=update_data)
    assert response.status_code == 400


def test_delete_post(app, client, user_for_test, post_for_test):
    response = client.delete(f'/posts/{post_for_test.id}')
    assert response.status_code == 204

    response = client.get(f'/posts/{post_for_test.id}')
    assert response.status_code == 404

def test_delete_post_404(app, client):
    response = client.delete(f'/posts/{uuid.uuid4()}')
    assert response.status_code == 404