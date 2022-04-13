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
def user3():
    credentials = base64.b64encode(b"user3:user3").decode('utf-8')
    user_headers = {"Authorization": f"Basic {credentials}"}
    return user_headers


@pytest.fixture(scope='module')
def user4():
    credentials = base64.b64encode(b"user4:user4").decode('utf-8')
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


class TestWallet:
    wallets = []

    def test_post_wallet_wrong_owner_id(self, user3):
        client = app.test_client()
        response = client.post('/wallets', data=json.dumps({
            "name": "User3 wallet",
            "fund": 0,
            "owner_id": "86bb9be4-42c5-4a2a-8ffe-5549cd06004"
        }), content_type='application/json', headers=user3)
        assert response.status_code == http.HTTPStatus.BAD_REQUEST

    def test_post_wallet_wrong_owner_id(self, user3):
        client = app.test_client()
        response = client.post('/wallets', data=json.dumps({
            "name": "User3 wallet",
            "funds": 0,
            "owner_id": "86bb9be4-42c5-4a2a-8ffe-5549cd06004"
        }), content_type='application/json', headers=user3)
        assert response.status_code == http.HTTPStatus.BAD_REQUEST

    def test_post_wallet_owner_id_no_permission(self, user3):
        client = app.test_client()
        response = client.post('/wallets', data=json.dumps({
            "name": "User3 wallet",
            "funds": 0,
            "owner_id": "b661d680-4c8d-4d42-9cbb-feaf9f5f2aaf"
        }), content_type='application/json', headers=user3)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_post_wallet_wrong_funds(self, user3):
        client = app.test_client()
        response = client.post('/wallets', data=json.dumps({
            "name": "User3 wallet",
            "funds": 1500,
            "owner_id": "86bb9be4-42c5-4a2a-8ffe-5549cd060044"
        }), content_type='application/json', headers=user3)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_post_wallet_for_user3(self, user3):
        client = app.test_client()
        response = client.post('/wallets', data=json.dumps({
            "name": "User3 wallet",
            "funds": 0,
            "owner_id": "86bb9be4-42c5-4a2a-8ffe-5549cd060044"
        }), content_type='application/json', headers=user3)
        self.wallets.append(response.json['uid'])
        assert response.status_code == http.HTTPStatus.CREATED

    def test_post_wallet_for_user3_wallet_exists(self, user3):
        client = app.test_client()
        response = client.post('/wallets', data=json.dumps({
            "name": "User3 wallet",
            "funds": 0,
            "owner_id": "86bb9be4-42c5-4a2a-8ffe-5549cd060044"
        }), content_type='application/json', headers=user3)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_post_wallet2_for_user3_wallet_exists(self, admin):
        client = app.test_client()
        response = client.post('/wallets', data=json.dumps({
            "name": "User3 monobank",
            "funds": 1500,
            "owner_id": "86bb9be4-42c5-4a2a-8ffe-5549cd060044"
        }), content_type='application/json', headers=admin)
        self.wallets.append(response.json['uid'])
        assert response.status_code == http.HTTPStatus.CREATED

    def test_post_wallet_for_user4(self, admin):
        client = app.test_client()
        response = client.post('/wallets', data=json.dumps({
            "name": "User4 wallet",
            "funds": 1500,
            "owner_id": "b661d680-4c8d-4d42-9cbb-feaf9f5f2aaf"
        }), content_type='application/json', headers=admin)
        self.wallets.append(response.json['uid'])
        assert response.status_code == http.HTTPStatus.CREATED

    def test_get_all_wallets(self, user3):
        client = app.test_client()
        response = client.get('/wallets', headers=user3)
        assert response.status_code == http.HTTPStatus.OK

    def test_get_wallet_no_permission(self, user3):
        client = app.test_client()
        response = client.get(f'/wallets/{self.wallets[-1]}', headers=user3)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_get_wallet_admin(self, admin):
        client = app.test_client()
        response = client.get(f'/wallets/{self.wallets[-1]}', headers=admin)
        assert response.status_code == http.HTTPStatus.OK

    def test_get_all_wallets_admin(self, admin):
        client = app.test_client()
        response = client.get(f'/wallets', headers=admin)
        assert response.status_code == http.HTTPStatus.OK

    def test_get_not_found_wallet_admin(self, admin):
        client = app.test_client()
        response = client.get(f'/wallets/12345', headers=admin)
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    def test_get_not_found_wallet_user4(self, user4):
        client = app.test_client()
        response = client.get(f'/wallets/12345', headers=user4)
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    def test_get_own_wallet_user4(self, user4):
        client = app.test_client()
        response = client.get(f'/wallets/{self.wallets[-1]}', headers=user4)
        assert response.status_code == http.HTTPStatus.OK

    def test_put_wallet_user3_no_permission(self, user3):
        client = app.test_client()
        response = client.put(f'/wallets/{self.wallets[-1]}', data=json.dumps({
            "name": "User3 monobank",
            "funds": 1500,
            "owner_id": "b661d680-4c8d-4d42-9cbb-feaf9f5f2aaf"
        }), content_type='application/json', headers=user3)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_put_wallet_user3_not_found(self, user3):
        client = app.test_client()
        response = client.put('/wallets/12345', data=json.dumps({
            "name": "User3 monobank",
            "funds": 1500,
            "owner_id": "b661d680-4c8d-4d42-9cbb-feaf9f5f2aaf"
        }), content_type='application/json', headers=user3)
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    def test_put_wallet_user3_wrong_funds(self, user3):
        client = app.test_client()
        response = client.put(f'/wallets/{self.wallets[0]}', data=json.dumps({
            "name": "User3 monobank",
            "funds": 1500,
            "owner_id": "86bb9be4-42c5-4a2a-8ffe-5549cd060044"
        }), content_type='application/json', headers=user3)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_put_wallet_user3_success(self, user3):
        client = app.test_client()
        response = client.put(f'/wallets/{self.wallets[0]}', data=json.dumps({
            "name": "User3 purse",
            "funds": 0,
            "owner_id": "86bb9be4-42c5-4a2a-8ffe-5549cd060044"
        }), content_type='application/json', headers=user3)
        assert response.status_code == http.HTTPStatus.OK

    def test_put_wallet_user3_admin(self, admin):
        client = app.test_client()
        response = client.put(f'/wallets/{self.wallets[0]}', data=json.dumps({
            "name": "User3 wallet",
            "funds": 1500,
            "owner_id": "86bb9be4-42c5-4a2a-8ffe-5549cd060044"
        }), content_type='application/json', headers=admin)
        assert response.status_code == http.HTTPStatus.OK

    def test_put_wallet_user3_admin_wrong_owner(self, admin):
        client = app.test_client()
        response = client.put(f'/wallets/{self.wallets[0]}', data=json.dumps({
            "name": "User3 wallet",
            "funds": 1500,
            "owner_id": "86bb9be4-42c5-4a2a-8ffe-5549cd0600"
        }), content_type='application/json', headers=admin)
        assert response.status_code == http.HTTPStatus.BAD_REQUEST

    def test_put_wallet_user3_admin_validation_error(self, admin):
        client = app.test_client()
        response = client.put(f'/wallets/{self.wallets[0]}', data=json.dumps({
            "na": "User3 wallet",
            "funds": 1500,
            "owner_id": "86bb9be4-42c5-4a2a-8ffe-5549cd0600"
        }), content_type='application/json', headers=admin)
        assert response.status_code == http.HTTPStatus.BAD_REQUEST

    def test_patch_wallet_user3_no_permission(self, user3):
        client = app.test_client()
        response = client.patch(f'/wallets/{self.wallets[-1]}', data=json.dumps({'name': 'Peshko Mono'}),
                                content_type='application/json', headers=user3)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_patch_wallet_user3_not_found(self, user3):
        client = app.test_client()
        response = client.patch(f'/wallets/12345', data=json.dumps({'name': 'Peshko Mono'}),
                                content_type='application/json', headers=user3)
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    def test_patch_wallet_user3_validation_error(self, user3):
        client = app.test_client()
        response = client.patch(f'/wallets/{self.wallets[0]}', data=json.dumps({'n': 'Peshko Mono'}),
                                content_type='application/json', headers=user3)
        assert response.status_code == http.HTTPStatus.BAD_REQUEST

    def test_patch_wallet_user3_wrong_funds(self, user3):
        client = app.test_client()
        response = client.patch(f'/wallets/{self.wallets[0]}', data=json.dumps({'funds': 9999}),
                                content_type='application/json', headers=user3)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_patch_wallet_user3_success(self, user3):
        client = app.test_client()
        response = client.patch(f'/wallets/{self.wallets[0]}', data=json.dumps({'name': 'User3 Privat'}),
                                content_type='application/json', headers=user3)
        assert response.status_code == http.HTTPStatus.OK

    def test_patch_wallet_admin(self, admin):
        client = app.test_client()
        response = client.patch(f'/wallets/{self.wallets[0]}', data=json.dumps({'name': 'User3 monobank'}),
                                content_type='application/json', headers=admin)
        assert response.status_code == http.HTTPStatus.OK

    def test_patch_wallet_admin_wrong_owner_id(self, admin):
        client = app.test_client()
        response = client.patch(f'/wallets/{self.wallets[0]}', data=json.dumps({'owner_id': '123'}),
                                content_type='application/json', headers=admin)
        assert response.status_code == http.HTTPStatus.BAD_REQUEST

    def test_delete_wallet_for_user3_no_permission(self, user3):
        client = app.test_client()
        response = client.delete(f'/wallets/9831-8579-5085-0885', headers=user3)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_delete_absent_wallet_for_user3(self, user3):
        client = app.test_client()
        response = client.delete(f'/wallets/1405-9700-8796-8219', headers=user3)
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    def test_delete_wallet_for_user3(self, user3):
        client = app.test_client()
        response = client.delete(f'/wallets/{self.wallets[0]}', headers=user3)
        assert response.status_code == http.HTTPStatus.NO_CONTENT

    def test_delete_wallet_for_user3_admin(self, admin):
        client = app.test_client()
        response = client.delete(f'/wallets/{self.wallets[1]}', headers=admin)
        assert response.status_code == http.HTTPStatus.NO_CONTENT

    def test_delete_wallet_for_user4_admin(self, admin):
        client = app.test_client()
        response = client.delete(f'/wallets/{self.wallets[-1]}', headers=admin)
        assert response.status_code == http.HTTPStatus.NO_CONTENT


class TestTransaction:
    wallets = []

    def test_post_wallet_for_user3(self, user3):
        client = app.test_client()
        response = client.post('/wallets', data=json.dumps({
            "name": "User3 wallet",
            "funds": 0,
            "owner_id": "86bb9be4-42c5-4a2a-8ffe-5549cd060044"
        }), content_type='application/json', headers=user3)
        self.wallets.append(response.json['uid'])
        assert response.status_code == http.HTTPStatus.CREATED

    def test_post_wallet_for_user4(self, admin):
        client = app.test_client()
        response = client.post('/wallets', data=json.dumps({
            "name": "User4 wallet",
            "funds": 1500,
            "owner_id": "b661d680-4c8d-4d42-9cbb-feaf9f5f2aaf"
        }), content_type='application/json', headers=admin)
        self.wallets.append(response.json['uid'])
        assert response.status_code == http.HTTPStatus.CREATED

    def test_post_transaction_user3_no_permission(self, user3):
        client = app.test_client()
        response = client.post('/transactions', data=json.dumps({
            "from_wallet_id": self.wallets[1],
            "to_wallet_id": self.wallets[0],
            "amount": 100
        }), content_type='application/json', headers=user3)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_post_transaction_user3_no_funds(self, user3):
        client = app.test_client()
        response = client.post('/transactions', data=json.dumps({
            "from_wallet_id": self.wallets[0],
            "to_wallet_id": self.wallets[1],
            "amount": 100
        }), content_type='application/json', headers=user3)
        assert response.status_code == http.HTTPStatus.BAD_REQUEST

    def test_post_transaction_admin(self, admin):
        client = app.test_client()
        response = client.post('/transactions', data=json.dumps({
            "from_wallet_id": self.wallets[1],
            "to_wallet_id": self.wallets[0],
            "amount": 10
        }), content_type='application/json', headers=admin)
        assert response.status_code == http.HTTPStatus.CREATED

    def test_post_transaction_wrong_from(self, admin):
        client = app.test_client()
        response = client.post('/transactions', data=json.dumps({
            "from_wallet_id": '12345',
            "to_wallet_id": self.wallets[0],
            "amount": 10
        }), content_type='application/json', headers=admin)
        assert response.status_code == http.HTTPStatus.BAD_REQUEST

    def test_post_transaction_wrong_to(self, admin):
        client = app.test_client()
        response = client.post('/transactions', data=json.dumps({
            "from_wallet_id": self.wallets[1],
            "to_wallet_id": '12345',
            "amount": 10
        }), content_type='application/json', headers=admin)
        assert response.status_code == http.HTTPStatus.BAD_REQUEST

    def test_post_transaction_validation_error(self, admin):
        client = app.test_client()
        response = client.post('/transactions', data=json.dumps({
            "from_wallet_": self.wallets[1],
            "to_wallet_id": self.wallets[0],
            "amount": 10
        }), content_type='application/json', headers=admin)
        assert response.status_code == http.HTTPStatus.BAD_REQUEST

    def test_post_transaction_user4(self, user4):
        client = app.test_client()
        response = client.post('/transactions', data=json.dumps({
            "from_wallet_id": self.wallets[1],
            "to_wallet_id": self.wallets[0],
            "amount": 10
        }), content_type='application/json', headers=user4)
        assert response.status_code == http.HTTPStatus.CREATED

    def test_get_transactions_user3_no_uid(self, user3):
        client = app.test_client()
        response = client.get('/transactions', headers=user3)
        assert response.status_code == http.HTTPStatus.OK

    def test_get_transactions_admin(self, admin):
        client = app.test_client()
        response = client.get('/transactions', headers=admin)
        assert response.status_code == http.HTTPStatus.OK

    def test_get_transactions_user3_no_permission(self, user3):
        client = app.test_client()
        response = client.get('/transactions/1', headers=user3)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_get_transactions_admin_by_uid(self, admin):
        client = app.test_client()
        response = client.get('/transactions/1', headers=admin)
        assert response.status_code == http.HTTPStatus.OK

    def test_get_transactions_user3_not_found(self, user3):
        client = app.test_client()
        response = client.get('/transactions/11111111', headers=user3)
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    def test_get_transactions_admin_not_found(self, admin):
        client = app.test_client()
        response = client.get('/transactions/11111111', headers=admin)
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    def test_delete_wallet_for_user3_admin(self, admin):
        client = app.test_client()
        response = client.delete(f'/wallets/{self.wallets[0]}', headers=admin)
        assert response.status_code == http.HTTPStatus.NO_CONTENT

    def test_delete_wallet_for_user4_admin(self, admin):
        client = app.test_client()
        response = client.delete(f'/wallets/{self.wallets[1]}', headers=admin)
        assert response.status_code == http.HTTPStatus.NO_CONTENT
