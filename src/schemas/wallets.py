from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.database.models import Wallet


class WalletSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Wallet
        exclude = ['uid']
        load_instance = True
        include_fk = True

