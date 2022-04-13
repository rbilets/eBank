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
