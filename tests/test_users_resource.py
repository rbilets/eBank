import http
import json

import pytest
from src import app
import base64


@pytest.fixture(scope='module')
def wrong_user():
    credentials = base64.b64encode(b"test:test").decode('utf-8')
    user_headers = {"Authorization": f"Basic {credentials}"}
    return user_headers


@pytest.fixture(scope='module')
def user1():
    credentials = base64.b64encode(b"user1:user1").decode('utf-8')
    user_headers = {"Authorization": f"Basic {credentials}"}
    return user_headers


@pytest.fixture(scope='module')
def user2():
    credentials = base64.b64encode(b"user2:user2").decode('utf-8')
    user_headers = {"Authorization": f"Basic {credentials}"}
    return user_headers


@pytest.fixture(scope='module')
def admin():
    credentials = base64.b64encode(b"romek_05:roman123").decode('utf-8')
    user_headers = {"Authorization": f"Basic {credentials}"}
    return user_headers


class TestUser:
    users = []

    def test_post_register_field_absent(self):
        client = app.test_client()
        response = client.post('/register', data=json.dumps({
            "email": "user1@gmail.com",
            "username": "user1",
            "password": "user1",
            "last_name": "one"
        }), content_type='application/json')
        assert response.status_code == http.HTTPStatus.BAD_REQUEST

    def test_post_register_username_exists(self):
        client = app.test_client()
        response = client.post('/register', data=json.dumps({
            "email": "user1@gmail.com",
            "username": "romek_05",
            "password": "user1",
            "first_name": "user1",
            "last_name": "one"
        }), content_type='application/json')
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_post_register_user1(self):
        client = app.test_client()
        response = client.post('/register', data=json.dumps({
            "email": "user1@gmail.com",
            "username": "user1",
            "password": "user1",
            "first_name": "user1",
            "last_name": "one"
        }), content_type='application/json')
        self.users.append(response.json['username'])
        assert response.status_code == http.HTTPStatus.OK

    def test_get_wrong_login(self, wrong_user):
        client = app.test_client()
        response = client.get('/login', headers=wrong_user)
        assert response.status_code == http.HTTPStatus.UNAUTHORIZED

    def test_get_correct_login(self, user1):
        client = app.test_client()
        response = client.get('/login', headers=user1)
        assert response.status_code == http.HTTPStatus.OK

    def test_get_all_users_admin(self, admin):
        client = app.test_client()
        response = client.get('/users', headers=admin)
        assert response.status_code == http.HTTPStatus.OK

    def test_get_user_by_correct_username_admin(self, admin):
        client = app.test_client()
        response = client.get('/users/user1', headers=admin)
        assert response.status_code == http.HTTPStatus.OK

    def test_get_user_by_wrong_username_admin(self, admin):
        client = app.test_client()
        response = client.get('/users/user11', headers=admin)
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    def test_get_users_for_simple_user(self, user1):
        client = app.test_client()
        response = client.get('/users', headers=user1)
        assert response.status_code == http.HTTPStatus.OK

    def test_get_users_for_simple_user_by_wrong_username(self, user1):
        client = app.test_client()
        response = client.get('/users/romek_05', headers=user1)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_get_users_for_simple_user_by_correct_username(self, user1):
        client = app.test_client()
        response = client.get('/users/user1', headers=user1)
        assert response.status_code == http.HTTPStatus.OK

    def test_post_user_user1_without_permission(self, user1):
        client = app.test_client()
        response = client.post('/users', data=json.dumps({
            "email": "user2@gmail.com",
            "username": "user2",
            "password": "user2",
            "first_name": "user2",
            "last_name": "two"
        }), content_type='application/json', headers=user1)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_post_user_admin_field_missing(self, admin):
        client = app.test_client()
        response = client.post('/users', data=json.dumps({
            "email": "user2@gmail.com",
            "username": "user2",
            "password": "user2",
            "last_name": "two"
        }), content_type='application/json', headers=admin)
        assert response.status_code == http.HTTPStatus.BAD_REQUEST

    def test_post_user_admin_email_exists(self, admin):
        client = app.test_client()
        response = client.post('/users', data=json.dumps({
            "email": "user1@gmail.com",
            "username": "user2",
            "password": "user2",
            "first_name": "user2",
            "last_name": "two"
        }), content_type='application/json', headers=admin)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_post_user_admin_success(self, admin):
        client = app.test_client()
        response = client.post('/users', data=json.dumps({
            "email": "user2@gmail.com",
            "username": "user2",
            "password": "user2",
            "first_name": "user2",
            "last_name": "two"
        }), content_type='application/json', headers=admin)
        self.users.append(response.json['username'])
        assert response.status_code == http.HTTPStatus.OK

    def test_put_user_user1_without_permission(self, user1):
        client = app.test_client()
        response = client.put('/users/user2', data=json.dumps({
            "email": "user2@gmail.com",
            "username": "user2",
            "password": "user2",
            "first_name": "user3",
            "last_name": "two"
        }), content_type='application/json', headers=user1)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_put_user_user1_with_permission_missing_field(self, user1):
        client = app.test_client()
        response = client.put('/users/user1', data=json.dumps({
            "email": "user1@gmail.com",
            "username": "user1",
            "password": "user1",
            "first_name": "user11",
        }), content_type='application/json', headers=user1)
        assert response.status_code == http.HTTPStatus.BAD_REQUEST

    def test_put_user_user1_with_permission_username_exists(self, user1):
        client = app.test_client()
        response = client.put('/users/user1', data=json.dumps({
            "email": "user2@gmail.com",
            "username": "user1",
            "password": "user1",
            "first_name": "user1",
            "last_name": "one"
        }), content_type='application/json', headers=user1)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_put_user_user1_with_permission(self, user1):
        client = app.test_client()
        response = client.put('/users/user1', data=json.dumps({
            "email": "user1@gmail.com",
            "username": "user1",
            "password": "user1",
            "first_name": "user11",
            "last_name": "Eleven"
        }), content_type='application/json', headers=user1)
        assert response.status_code == http.HTTPStatus.OK

    def test_put_user_user1_admin(self, admin):
        client = app.test_client()
        response = client.put('/users/user1', data=json.dumps({
            "email": "user1@gmail.com",
            "username": "user1",
            "password": "user1",
            "first_name": "user1",
            "last_name": "one"
        }), content_type='application/json', headers=admin)
        assert response.status_code == http.HTTPStatus.OK

    def test_put_user_wrong_user_admin(self, admin):
        client = app.test_client()
        response = client.put('/users/wrong_user', data=json.dumps({
            "email": "user1@gmail.com",
            "username": "user1",
            "password": "user1",
            "first_name": "user1",
            "last_name": "one"
        }), content_type='application/json', headers=admin)
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    def test_patch_user_user1_without_permission(self, user1):
        client = app.test_client()
        response = client.patch('/users/user2', data=json.dumps({
            "first_name": "user3"
        }), content_type='application/json', headers=user1)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_patch_user_user1_with_permission_email_exists(self, user1):
        client = app.test_client()
        response = client.patch('/users/user1', data=json.dumps({
            "email": "user2@gmail.com"
        }), content_type='application/json', headers=user1)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_patch_wrong_user_admin(self, admin):
        client = app.test_client()
        response = client.patch('/users/user22', data=json.dumps({
            "first_name": "user2"
        }), content_type='application/json', headers=admin)
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    def test_patch_user_user2_with_permission(self, user1):
        client = app.test_client()
        response = client.patch('/users/user1', data=json.dumps({
            "first_name": "user11"
        }), content_type='application/json', headers=user1)
        assert response.status_code == http.HTTPStatus.OK

    def test_patch_user_admin(self, admin):
        client = app.test_client()
        response = client.patch('/users/user1', data=json.dumps({
            "first_name": "user1"
        }), content_type='application/json', headers=admin)
        assert response.status_code == http.HTTPStatus.OK

    def test_patch_user_admin_wrong_field(self, admin):
        client = app.test_client()
        response = client.patch('/users/user1', data=json.dumps({
            "first_n": "user1"
        }), content_type='application/json', headers=admin)
        assert response.status_code == http.HTTPStatus.BAD_REQUEST

    def test_delete_wrong_user(self, admin):
        client = app.test_client()
        response = client.delete(f'/users/wrong_user', headers=admin)
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    def test_delete_user1_no_permission(self, user2):
        client = app.test_client()
        response = client.delete(f'/users/{self.users[0]}', headers=user2)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_delete_user1_admin(self, admin):
        client = app.test_client()
        response = client.delete(f'/users/{self.users[0]}', headers=admin)
        assert response.status_code == http.HTTPStatus.NO_CONTENT

    def test_delete_user2_with_permission(self, admin):
        client = app.test_client()
        response = client.delete(f'/users/{self.users[1]}', headers=admin)
        assert response.status_code == http.HTTPStatus.NO_CONTENT

