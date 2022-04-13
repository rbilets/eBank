from src import api
# from src.resources.auth import AuthRegister, AuthLogin
from src.resources.auth import AuthRegister, AuthLogin, AuthLogout, Profile
from src.resources.transactions import TransactionListApiGet, TransactionListApiPost
from src.resources.users import UserListApiGet, UserListApiUpdate, UserListApiPost, UserListApiDelete
from src.resources.smoke import Smoke
from src.resources.wallets import WalletListApiGet, WalletListApiPost, WalletListApiEdit, WalletListApiDelete

api.add_resource(AuthRegister, '/register', strict_slashes=False)
api.add_resource(AuthLogin, '/login', strict_slashes=False)
api.add_resource(AuthLogout, '/logout', strict_slashes=False)
api.add_resource(Profile, '/profile', strict_slashes=False)
api.add_resource(UserListApiGet, '/users', '/users/<username>', strict_slashes=False)
api.add_resource(UserListApiUpdate, '/editUser/<username>', strict_slashes=False)
api.add_resource(UserListApiPost, '/addUser', strict_slashes=False)
api.add_resource(UserListApiDelete, '/deleteUser/<username>', strict_slashes=False)
api.add_resource(Smoke, '/', strict_slashes=False)
api.add_resource(WalletListApiGet, '/wallets', '/wallets/<uid>', strict_slashes=False)
api.add_resource(WalletListApiPost, '/walletCreate', strict_slashes=False)
api.add_resource(WalletListApiEdit, '/walletEdit/<uid>', strict_slashes=False)
api.add_resource(WalletListApiDelete, '/walletDelete/<uid>', strict_slashes=False)
api.add_resource(TransactionListApiGet, '/transactions', '/transactions/<uid_username>', strict_slashes=False)
api.add_resource(TransactionListApiPost, '/transactionsPost', '/transactionsPost/<uid_username>', strict_slashes=False)

# curl --location --request GET 'http://127.0.0.1:5000/wallets' \
# --header 'x-api-key: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYTJkNjA4YmMtY2ViYi00M2FiLThlZTQtMGNjN2NjY2Y5ZjU1IiwiZXhwIjoxNjM2NTMwMTY2fQ.-Hkmzj7L8VOOEGfFoIm7HGob0UvuC_9s-PIr6vGaCe0'

# curl -u romek_05:roman123 -i -X GET http://127.0.0.1:5000/wallets/


# {}
# ___________________________POST___________________________

# curl --location --request POST 'http://127.0.0.1:5000/register' \
# --header 'Content-Type: application/json' \
# --data-raw '{
#     "email": "maddir_repka@gmail.com",
#     "username": "maddie",
#     "password": "repka",
#     "first_name": "Maddie",
#     "last_name": "Repka"
# }'

#
# curl --location --request POST 'http://127.0.0.1:5000/wallets' \
# --header 'Content-Type: application/json' \
# --data-raw '{
#     "name": "Oleh money",
#     "funds": 2500,
#     "owner_id": "ff1c6c50-3551-479c-a910-c70986a695c0"
# }'

# curl --location --request POST 'http://127.0.0.1:5000/transactions' \
# --header 'Content-Type: application/json' \
# --data-raw '{
#     "amount": 500.2,
#     "from_wallet_id": "9676-5144-5895-9374",
#     "to_wallet_id": "7203-5400-7828-0257"
# }'


# ___________________________PUT___________________________

# curl --location --request PUT 'http://127.0.0.1:5000/users/oleh_mal' \
# --header 'Content-Type: application/json' \
# --data-raw '{
#     "email": "oleh_maletskiy@gmail.com",
#     "username": "oleh_mal",
#     "password": "olko123",
#     "first_name": "Olezhyk",
#     "last_name": "Maletskyi"
# }'

# curl --location --request PUT 'http://127.0.0.1:5000/wallets/1374-8405-0554-1780' \
# --header 'Content-Type: application/json' \
# --data-raw '{
#     "name": "Maddie copilka",
#     "funds": 2000,
#     "owner_id": 4
# }'


# ___________________________PATCH___________________________
#
# curl --location --request PATCH 'http://127.0.0.1:5000/users/4' \
# --header 'Content-Type: application/json' \
# --data-raw '{
#     "first_name": "Maddie"
# }'

# curl --location --request PATCH 'http://127.0.0.1:5000/wallets/1374-8405-0154-1780' \
# --header 'Content-Type: application/json' \
# --data-raw '{
#     "funds": 3000
# }'


# ___________________________DELETE___________________________
# curl --location --request DELETE 'http://127.0.0.1:5000/users/4' \
# --header 'Content-Type: application/json' \
# --data-raw '{}'
#
# curl --location --request DELETE 'http://127.0.0.1:5000/wallets/9495-0115-2953-0500' \
# --header 'Content-Type: application/json' \
# --data-raw '{}'
