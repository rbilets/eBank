import http

from src import app


def test_smoke():
    client = app.test_client()
    resp = client.get('/smoke')
    assert resp.status_code == http.HTTPStatus.OK

import http
import json

import pytest
from src import app
import base64


@pytest.fixture(scope='module')
def user():
    credentials = base64.b64encode(b"sheva123:andriy123").decode('utf-8')
    user_headers = {"Authorization": f"Basic {credentials}"}
    return user_headers


@pytest.fixture(scope='module')
def user_maddie():
    credentials = base64.b64encode(b"maddie:repka").decode('utf-8')
    user_headers = {"Authorization": f"Basic {credentials}"}
    return user_headers


@pytest.fixture(scope='module')
def wrong_user():
    credentials = base64.b64encode(b"sheva12:andriy12").decode('utf-8')
    user_headers = {"Authorization": f"Basic {credentials}"}
    return user_headers


@pytest.fixture(scope='module')
def admin():
    credentials = base64.b64encode(b"romek_05:roman123").decode('utf-8')
    user_headers = {"Authorization": f"Basic {credentials}"}
    return user_headers


@pytest.fixture(scope='module')
def new_user_maddie():
    user = {
        "email": "maddie_repka@gmail.com",
        "username": "maddie",
        "password": "repka",
        "first_name": "Maddie",
        "last_name": "Repka"
    }
    return json.dumps(user)


@pytest.fixture(scope='module')
def updated_user_maddie():
    user = {
        "email": "romek_05@gmail.com",
        "username": "maddie",
        "password": "repka",
        "first_name": "Maddeline",
        "last_name": "Repochka"
    }
    return json.dumps(user)


@pytest.fixture(scope='module')
def new_user_petro():
    user = {
        "email": "petro_repka@gmail.com",
        "username": "petro",
        "password": "petro",
        "first_name": "Petro",
        "last_name": "Repka"
    }
    return json.dumps(user)


class TestUser:
    users = []

    def test_post_register_with_db(self, new_user_maddie):
        client = app.test_client()
        response = client.post('/register', data=new_user_maddie, content_type='application/json')
        assert response.status_code == http.HTTPStatus.OK
        assert response.json['username'] == 'maddie'
        self.users.append(response.json['username'])

    def test_get_correct_login_with_db(self, user):
        client = app.test_client()
        response = client.get('/login', headers=user)
        assert response.status_code == http.HTTPStatus.OK

    def test_get_wrong_login_with_db(self, wrong_user):
        client = app.test_client()
        response = client.get('/login', headers=wrong_user)
        assert response.status_code == http.HTTPStatus.UNAUTHORIZED

    def test_get_users_for_wrong_user_with_db(self, wrong_user):
        client = app.test_client()
        response = client.get('/users', headers=wrong_user)
        assert response.status_code == http.HTTPStatus.UNAUTHORIZED

    def test_get_user_for_user_without_permission_with_db(self, user):
        client = app.test_client()
        response = client.get('/users/romek_05', headers=user)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_get_users_for_admin_with_db(self, admin):
        client = app.test_client()
        response = client.get('/users', headers=admin)
        assert response.status_code == http.HTTPStatus.OK

    def test_get_user_for_admin_with_db(self, admin):
        client = app.test_client()
        response = client.get('/users/sheva123', headers=admin)
        assert response.status_code == http.HTTPStatus.OK

    def test_get_users_for_user_with_permission_with_db(self, user):
        client = app.test_client()
        response = client.get('/users', headers=user)
        assert response.status_code == http.HTTPStatus.OK

    def test_get_user_for_user_with_permission_with_db(self, user):
        client = app.test_client()
        response = client.get('/users/sheva123', headers=user)
        assert response.status_code == http.HTTPStatus.OK

    def test_post_user_for_user_without_permission_with_db(self, new_user_petro, user):
        client = app.test_client()
        response = client.post('/users', data=new_user_petro, content_type='application/json', headers=user)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_post_user_for_admin_with_permission_with_db(self, new_user_petro, admin):
        client = app.test_client()
        response = client.post('/users', data=new_user_petro, content_type='application/json', headers=admin)
        assert response.status_code == http.HTTPStatus.OK
        assert response.json['username'] == 'petro'
        self.users.append(response.json['username'])

    def test_put_user_for_user_without_permission_with_db(self, user, updated_user_maddie):
        client = app.test_client()
        response = client.put('/users/maddie', data=updated_user_maddie, content_type='application/json', headers=user)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_put_user_for_admin_with_permission_with_db(self, admin, updated_user_maddie):
        client = app.test_client()
        response = client.put('/users/maddie', data=updated_user_maddie, content_type='application/json', headers=admin)
        assert response.status_code == http.HTTPStatus.OK

    def test_patch_email_for_user_without_permission_with_db(self, user):
        client = app.test_client()
        response = client.patch('/users/maddie', data={'email': 'mad_repka@gmail.com'}, content_type='application/json',
                                headers=user)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_patch_name_for_user_with_permission_with_db(self, user_maddie):
        client = app.test_client()
        response = client.patch('/users/maddie', data=json.dumps({'first_name': 'Madeline'}), content_type='application/json',
                                headers=user_maddie)
        assert response.status_code == http.HTTPStatus.OK

    def test_patch_name_for_admin_with_permission_with_db(self, admin):
        client = app.test_client()
        response = client.patch('/users/maddie', data=json.dumps({'first_name': 'Maddie'}), content_type='application/json',
                                headers=admin)
        assert response.status_code == http.HTTPStatus.OK

    def test_delete_user_maddie_for_user_without_permission_with_db(self, user):
        client = app.test_client()
        response = client.delete(f'/users/maddie', headers=user)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_delete_user_maddie_for_user_with_permission_with_db(self, admin):
        client = app.test_client()
        response = client.delete(f'/users/maddie', headers=admin)
        assert response.status_code == http.HTTPStatus.NO_CONTENT

    def test_delete_user_petro_for_admin_with_db(self, admin):
        client = app.test_client()
        response = client.delete(f'/users/petro', headers=admin)
        assert response.status_code == http.HTTPStatus.NO_CONTENT

#__________________

import http
import json

import pytest
from src import app
import base64


@pytest.fixture(scope='module')
def user():
    credentials = base64.b64encode(b"sheva123:andriy123").decode('utf-8')
    user_headers = {"Authorization": f"Basic {credentials}"}
    return user_headers


@pytest.fixture(scope='module')
def user_peshko():
    credentials = base64.b64encode(b"maskpesh:maksym123").decode('utf-8')
    user_headers = {"Authorization": f"Basic {credentials}"}
    return user_headers


@pytest.fixture(scope='module')
def wrong_user():
    credentials = base64.b64encode(b"sheva12:andriy12").decode('utf-8')
    user_headers = {"Authorization": f"Basic {credentials}"}
    return user_headers


@pytest.fixture(scope='module')
def admin():
    credentials = base64.b64encode(b"romek_05:roman123").decode('utf-8')
    user_headers = {"Authorization": f"Basic {credentials}"}
    return user_headers


@pytest.fixture(scope='module')
def new_wallet_sheva_wrong_funds():
    user = {
        "name": "Sheva Wallet",
        "funds": 2500,
        "owner_id": "626edbc9-97c7-455b-8e7d-6378a8ad9303"
    }
    return json.dumps(user)


@pytest.fixture(scope='module')
def new_wallet_sheva():
    user = {
        "name": "Sheva Purse",
        "funds": 0,
        "owner_id": "626edbc9-97c7-455b-8e7d-6378a8ad9303"
    }
    return json.dumps(user)


@pytest.fixture(scope='module')
def new_wallet_peshko():
    user = {
        "name": "Peshko Wallet 2",
        "funds": 2000,
        "owner_id": "7e43a988-5d0f-4897-b1c7-20c1b668510f"
    }
    return json.dumps(user)


@pytest.fixture(scope='module')
def updated_wallet_peshko():
    user = {
        "name": "Peshko Monobank",
        "funds": 4500,
        "owner_id": "7e43a988-5d0f-4897-b1c7-20c1b668510f"
    }
    return json.dumps(user)


class TestWallet:
    wallets = []

    def test_get_wallets_for_user_without_permission_with_db(self, user):
        client = app.test_client()
        response = client.get('/wallets/6630-9813-6347-3455', headers=user)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_get_wallets_for_user_with_permission_with_db(self, user):
        client = app.test_client()
        response = client.get('/wallets/2667-8220-4147-7929', headers=user)
        assert response.status_code == http.HTTPStatus.OK

    def test_get_wallets_for_admin_with_permission_with_db(self, admin):
        client = app.test_client()
        response = client.get('/wallets', headers=admin)
        assert response.status_code == http.HTTPStatus.OK

    def test_post_wallet_for_user_wrong_funds_with_db(self, new_wallet_sheva_wrong_funds, user):
        client = app.test_client()
        response = client.post('/wallets', data=new_wallet_sheva_wrong_funds, content_type='application/json', headers=user)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_post_wallet_for_user_correct_funds_with_db(self, new_wallet_sheva, user):
        client = app.test_client()
        response = client.post('/wallets', data=new_wallet_sheva, content_type='application/json', headers=user)
        assert response.status_code == http.HTTPStatus.CREATED

    # def test_post_wallet_for_admin_with_db(self, new_wallet_peshko, admin):
    #     client = app.test_client()
    #     response = client.post('/wallets', data=new_wallet_peshko, content_type='application/json', headers=admin)
    #     assert response.status_code == http.HTTPStatus.CREATED

    def test_put_wallet_for_user_without_permission_with_db(self, updated_wallet_peshko, user):
        client = app.test_client()
        response = client.put('/wallets/7837-9542-4713-8174', data=updated_wallet_peshko,
                              content_type='application/json', headers=user)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_put_wallet_for_user_with_permission_wrong_funds_with_db(self, updated_wallet_peshko, user_peshko):
        client = app.test_client()
        response = client.put('/wallets/7837-9542-4713-8174', data=updated_wallet_peshko,
                              content_type='application/json', headers=user_peshko)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_put_wallet_for_admin_with_db(self, updated_wallet_peshko, admin):
        client = app.test_client()
        response = client.put('/wallets/7837-9542-4713-8174', data=updated_wallet_peshko,
                              content_type='application/json', headers=admin)
        assert response.status_code == http.HTTPStatus.OK

    def test_patch_wallet_name_for_user_without_permission_with_db(self, user):
        client = app.test_client()
        response = client.patch('/wallets/7837-9542-4713-8174', data=json.dumps({'name': 'Buying a car'}), content_type='application/json',
                                headers=user)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_patch_wallet_name_for_user_with_permission_with_db(self, user_peshko):
        client = app.test_client()
        response = client.patch('/wallets/7837-9542-4713-8174', data=json.dumps({'name': 'Buying a car'}), content_type='application/json',
                                headers=user_peshko)
        assert response.status_code == http.HTTPStatus.OK

    def test_patch_wallet_name_for_admin_with_db(self, admin):
        client = app.test_client()
        response = client.patch('/wallets/7837-9542-4713-8174', data=json.dumps({'name': 'Peshko Mono'}), content_type='application/json',
                                headers=admin)
        assert response.status_code == http.HTTPStatus.OK

    def test_delete_wallet_for_user_without_permission_with_db(self, user):
        client = app.test_client()
        response = client.delete(f'/wallets/6630-9813-6347-3455',  headers=user)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_delete_wallet_for_user_with_permission_last_wallet_with_db(self, user_peshko):
        client = app.test_client()
        response = client.delete(f'/wallets/7837-9542-4713-8174',  headers=user_peshko)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_delete_wallet_for_admin_last_wallet_with_db(self, admin):
        client = app.test_client()
        response = client.delete(f'/wallets/7837-9542-4713-8174',  headers=admin)
        assert response.status_code == http.HTTPStatus.CONFLICT

    # def test_delete_wallet_for_user_with_permission_with_db(self, user):
    #     client = app.test_client()
    #     response = client.delete(f'/wallets/{self.wallets[0]}',  headers=user)
    #     assert response.status_code == http.HTTPStatus.NO_CONTENT
    # #
    # def test_delete_wallet_for_admin_with_db(self, admin):
    #     client = app.test_client()
    #     response = client.delete(f'/wallets/7332-1849-7680-5426',  headers=admin)
    #     assert response.status_code == http.HTTPStatus.NO_CONTENT


#_______________________
import http
import json

import pytest
from src import app
import base64


@pytest.fixture(scope='module')
def user():
    credentials = base64.b64encode(b"sheva123:andriy123").decode('utf-8')
    user_headers = {"Authorization": f"Basic {credentials}"}
    return user_headers


@pytest.fixture(scope='module')
def user_peshko():
    credentials = base64.b64encode(b"maskpesh:maksym123").decode('utf-8')
    user_headers = {"Authorization": f"Basic {credentials}"}
    return user_headers


@pytest.fixture(scope='module')
def wrong_user():
    credentials = base64.b64encode(b"sheva12:andriy12").decode('utf-8')
    user_headers = {"Authorization": f"Basic {credentials}"}
    return user_headers


@pytest.fixture(scope='module')
def admin():
    credentials = base64.b64encode(b"romek_05:roman123").decode('utf-8')
    user_headers = {"Authorization": f"Basic {credentials}"}
    return user_headers


@pytest.fixture(scope='module')
def new_transaction():
    transaction = {
        "amount": 50,
        "from_wallet_id": "2667-8220-4147-7929",
        "to_wallet_id": "6630-9813-6347-3455"
    }
    return json.dumps(transaction)


class TestTransaction:
    transactions = []

    def test_get_transactions_for_user_without_permission_with_db(self, user):
        client = app.test_client()
        response = client.get('/transactions/2', headers=user)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_get_transactions_for_user_with_permission_with_db(self, user):
        client = app.test_client()
        response = client.get('/transactions/1', headers=user)
        assert response.status_code == http.HTTPStatus.OK

    def test_get_transactions_for_admin_with_db(self, admin):
        client = app.test_client()
        response = client.get('/transactions/1', headers=admin)
        assert response.status_code == http.HTTPStatus.OK

    def test_post_transaction_for_user_without_permission_with_db(self, new_transaction, user_peshko):
        client = app.test_client()
        response = client.post('/transactions', data=new_transaction, content_type='application/json',
                               headers=user_peshko)
        assert response.status_code == http.HTTPStatus.CONFLICT

    def test_post_transaction_for_admin_with_db(self, new_transaction, admin):
        client = app.test_client()
        response = client.post('/transactions', data=new_transaction, content_type='application/json',
                               headers=admin)
        assert response.status_code == http.HTTPStatus.CREATED

    def test_post_transaction_for_user_with_permission_with_db(self, new_transaction, user):
        client = app.test_client()
        response = client.post('/transactions', data=new_transaction, content_type='application/json',
                               headers=user)
        assert response.status_code == http.HTTPStatus.CREATED
