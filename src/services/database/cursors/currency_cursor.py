from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.services.database.models.currency_model import Currency


class NotEnoughCurrency:
    pass


db = 'sqlite:///db/file.db'

engine = create_engine(db)
Session = sessionmaker()


# TODO: update currency table
class ModifyCurrency:
    def new_currency(self, user_id: int):
        session = Session()

        insert = Currency(guild=user_id, amount=0)

        session.add(insert)
        session.commit()

    def add_currency(self, user_id: int, amount: int):
        session = Session()

        currency = self.get_currency(user_id)
        currency.amount = currency.amount + amount

        session.commit()

    def take_currency(self, user_id: int, amount: int):
        session = Session()

        currency = self.get_currency(user_id)
        currency.amount = currency.amount - amount

        # Make sure amount doesn't get under 0.
        if currency.amount < 0:
            currency.amount = 0

        session.commit()

    def transfer_currency(self, from_id: int, to_id: int, amount: int):
        if not self.get_currency(from_id) <= amount:
            self.take_currency(from_id, amount)
            self.add_currency(to_id, amount)
        else:
            raise NotEnoughCurrency

    def get_currency(self, user_id: int):
        return Currency.query.filter_by(snowflake=user_id).first()
