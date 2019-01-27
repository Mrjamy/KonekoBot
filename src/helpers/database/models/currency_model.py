from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from src.core.exceptions import NotEnoughBalance
from src.helpers.database.entities import currency as table


class Currency:
    def __init__(self):
        db_uri = 'sqlite:///src/core/data/currency.sqlite'

        self.engine = create_engine(db_uri)
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

    def get(self, user_id: int, guild_id: int)->table:
        balance = self.session.query(table.Currency) \
            .filter(
            table.Currency.snowflake == user_id,
            table.Currency.guild == guild_id
        ) \
            .first()
        if balance is None:
            balance = self.insert(user_id, guild_id)
        return balance

    def get_all(self, guild_id: int, offset: int = 0):
        return self.session.query(table.Currency) \
            .filter(
            table.Currency.guild == guild_id
        ) \
            .order_by(
            table.Currency.amount.desc()
        ) \
            .limit(10) \
            .offset(offset) \
            .all()

    def update(self, user_id: int, guild_id: int, amount: int = +100)->table:
        def check():
            if not bool(self.get(user_id, guild_id).amount >= amount):
                raise NotEnoughBalance

        # Check if a user has the funds to proceed
        if amount < 0:
            check()

        user = self.get(user_id, guild_id)
        user.amount += amount
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            print(e)
            return
        return user

    def insert(self, user_id: int, guild_id: int)->table:
        currency = table.Currency()
        currency.snowflake = user_id
        currency.guild = guild_id
        currency.amount = 0
        try:
            self.session.add(currency)
            self.session.commit()
        except SQLAlchemyError as e:
            print(e)
            return
        return currency
