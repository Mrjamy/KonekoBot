from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import INTEGER, TEXT, TIMESTAMP

Base = declarative_base()


class Level(Base):
    __tablename__ = 'levels'
    __table_args__ = {'sqlite_autoincrement': True}
    snowflake = Column(TEXT, nullable=False)
    guild = Column(TEXT, nullable=False)
    experience = Column(INTEGER, nullable=False)
    level = Column(INTEGER, nullable=False)
    last_message = Column(TIMESTAMP, nullable=False)
