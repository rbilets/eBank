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
