from src import db
from src.database.models import User, Wallet, Transaction


def populate_db():
    user_1 = User(email='andriy_shevchenko@gmail.com', username='sheva123', password='andriy123', first_name='Andriy',
                  last_name='Shevchenko')

    user_2 = User(email='roman.bilets@icloud.com', username='romek_05', password='roman123', first_name='Roman',
                  last_name='Bilets', is_admin=True)

    user_3 = User(email='maksym_peshko@gmail.com', username='maskpesh', password='maksym123', first_name='Maksym',
                  last_name='Peshko')

    wallet_1 = Wallet(name='My Wallet', funds=1000.5, owner_id=user_1.uid)
    wallet_2 = Wallet(name='Romek Visa', funds=2100.2, owner_id=user_2.uid)
    wallet_3 = Wallet(name='Buying a car', funds=500, owner_id=user_3.uid)
    wallet_4 = Wallet(name='Romek Mastercard', funds=3100, owner_id=user_2.uid)

    transaction_1 = Transaction(from_wallet_id=wallet_1.uid, to_wallet_id=wallet_2.uid, amount=300)
    transaction_1.status = 1
    transaction_2 = Transaction(from_wallet_id=wallet_2.uid, to_wallet_id=wallet_3.uid, amount=210)
    transaction_2.status = 0
    transaction_3 = Transaction(from_wallet_id=wallet_3.uid, to_wallet_id=wallet_4.uid, amount=600)
    transaction_3.status = 1

    db.session.add(user_1)
    db.session.add(user_2)
    db.session.add(user_3)

    db.session.add(wallet_1)
    db.session.add(wallet_2)
    db.session.add(wallet_3)
    db.session.add(wallet_4)

    db.session.add(transaction_1)
    db.session.add(transaction_2)
    db.session.add(transaction_3)

    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    print('Populating db...')
    populate_db()
    print('Successfully populated!')
