import random
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from src.helpers.database.entities import level as table


class Level:
    def __init__(self):
        db_uri = 'sqlite:///src/core/data/level.sqlite'

        self.engine = create_engine(db_uri)
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

    def get(self, user_id: int, guild_id: int)->table:
        level = self.session.query(table.Level) \
            .filter(
                table.Level.snowflake == user_id,
                table.Level.guild == guild_id
            ) \
            .first()
        if level is None:
            level = self.insert(user_id, guild_id)
        return level

    def get_all(self, guild_id: int, offset: int = 0):
        return self.session.query(table.Level) \
            .filter(
                table.Level.guild == guild_id
            ) \
            .order_by(
                table.Level.experience.desc()
            ) \
            .limit(10) \
            .offset(offset) \
            .all()

    def add(self, user_id: int, guild_id: int)->table:
        def _cooldown():
            return (datetime.now() - level.last_message).total_seconds() < 30

        level = self.session.query(table.Level) \
            .filter(
                table.Level.snowflake == user_id,
                table.Level.guild == guild_id
            ) \
            .first()
        if level is None:
            level = self.insert(user_id, guild_id)

        if not _cooldown():
            level.experience += random.randint(5, 10)
            level.last_message = datetime.now()
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            print(e)
            return
        return level

    def insert(self, user_id: int, guild_id: int)->table:
        level = table.Level()
        level.snowflake = user_id
        level.guild = guild_id
        level.experience = 0
        level.level = 0
        try:
            self.session.add(level)
            self.session.commit()
        except SQLAlchemyError as e:
            print(e)
            return
        return level

    def levelup_check(self, user_id: int, guild_id: int)->bool:
        level = self.get(user_id, guild_id)

        experience = level.experience
        lvl_start = level.level
        lvl_end = int(experience ** (1 / 4))

        up = False
        if lvl_start < lvl_end:
            level.level = lvl_end
            up = True

        try:
            self.session.commit()
        except SQLAlchemyError as e:
            print(e)
            return False
        return up
