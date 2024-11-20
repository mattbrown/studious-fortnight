import pytest
from microblog import create_app
from microblog import db
from microblog.models import User
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
def test_user(app):
    with app.app_context():
        test_user = User(name="test_get_guy", email="test@example.com")
        db.session.add(test_user)
        db.session.commit()
        yield test_user


def test_get_all_users(app, client):
    with app.app_context():
        test_user = User(name="test_guy", email="test@example.com")
        db.session.add(test_user)
        db.session.commit()

    response = client.get("/users").get_json()

    assert len(response) == 1
    assert response[0]['name'] == "test_guy"
    assert response[0]['email'] == "test@example.com"
    assert 'id' in response[0]


def test_post_users(app, client):
    test_user = {
        'name': 'test_post',
        'email': 'post@example.com'
    }

    response = client.post('/users', json=test_user)

    assert response.status_code == 200
    assert response.get_json()['name'] == 'test_post'
    assert response.get_json()['email'] == 'post@example.com'


def test_get_user(app, client, test_user):
    response = client.get(f'/users/{test_user.id}')

    assert response.status_code == 200
    assert response.get_json()['id'] == str(test_user.id)
    assert response.get_json()['name'] == test_user.name


def test_get_user_404(app, client):
    response = client.get(f'/users/{uuid.uuid4()}')

    assert response.status_code == 404


def test_update_user(app, client, test_user):
    user_data = test_user.to_dict()
    user_data['name'] = 'bloop'

    response = client.put(f'/users/{test_user.id}', json=user_data)
    assert response.status_code == 200

    response = client.get(f'/users/{test_user.id}')
    assert response.status_code == 200
    assert response.get_json()['name'] == 'bloop'


def test_update_user_404(app, client):
    update_dict = {
        'name': 'sir not appearing in this film',
        'email': 'monty@example.com'
    }
    response = client.put(f'/users/{uuid.uuid4()}', json = update_dict)
    assert response.status_code == 404


def test_delete_user(app, client, test_user):
    response = client.delete(f'/users/{test_user.id}')
    assert response.status_code == 204

    response = client.get(f'/users/{test_user.id}')
    assert response.status_code == 404


def test_delete_user_404(app, client):
    response = client.delete(f'/users/{uuid.uuid4()}')
    assert response.status_code == 404
