from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.database.models import Transaction


class TransactionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Transaction
        exclude = ['status']
        load_instance = True
        include_fk = True
