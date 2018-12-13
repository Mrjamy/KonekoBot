from sqlalchemy import (
    Column,
    create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import INTEGER, TEXT


db_uri = 'sqlite:///src/core/data/currency.sqlite'
engine = create_engine(db_uri)

Base = declarative_base()


class Currency(Base):
    __tablename__ = 'currency'
    __table_args__ = {'sqlite_autoincrement': True}
    snowflake = Column(INTEGER, nullable=False, primary_key=True)
    guild = Column(INTEGER, nullable=False)
    amount = Column(TEXT, nullable=False)


Base.metadata.create_all(engine)
