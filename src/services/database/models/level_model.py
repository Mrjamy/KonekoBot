import time
from sqlalchemy import (
    Column,
    create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import INTEGER, TEXT, TIMESTAMP


db_uri = 'sqlite:///level.sqlite'
engine = create_engine(db_uri)

Base = declarative_base()


class Level(Base):
    __tablename__ = 'levels'
    __table_args__ = {'sqlite_autoincrement': True}
    snowflake = Column(TEXT, nullable=False, primary_key=True)
    guild = Column(TEXT, nullable=False)
    experience = Column(INTEGER, nullable=False)
    level = Column(INTEGER, nullable=False)
    last_message = Column(TIMESTAMP, nullable=False, default=time.time())


Base.metadata.create_all(engine)
