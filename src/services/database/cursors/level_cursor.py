from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.services.database.models.level_model import Level

db = 'sqlite:///db/file.db'

engine = create_engine(db)
Session = sessionmaker()


# TODO: update currency table
class ModifyCurrency:
    def new_xp(self, user_id: int):
        insert = Level(guild=user_id, amount=0)
        session = Session()

        session.add(insert)

    def add_xp(self, user_id: int, amount: int):
        session = Session()

        xp = self.get_xp(user_id)
        xp.experience = xp.experience + amount

        session.commit()

    def get_xp(self, user_id: int):
        return Level.query.filter_by(snowflake=user_id).first()
