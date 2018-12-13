import datetime
from sqlalchemy import (
    Column,
    create_engine
)
from sqlalchemy.dialects.sqlite import (
    INTEGER,
    TEXT,
    DATETIME
)
from sqlalchemy.ext.declarative import declarative_base


db_uri = 'sqlite:///src/core/data/level.sqlite'
engine = create_engine(db_uri)

Base = declarative_base()


class Level(Base):
    __tablename__ = 'levels'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(INTEGER, nullable=False, primary_key=True)
    snowflake = Column(TEXT, nullable=False)
    guild = Column(TEXT, nullable=False)
    experience = Column(INTEGER, nullable=False, default=0)
    level = Column(INTEGER, nullable=False, default=1)
    last_message = Column(DATETIME, nullable=False, default=datetime.datetime.now())


Base.metadata.create_all(engine)
