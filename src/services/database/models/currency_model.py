from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import INTEGER, TEXT

Base = declarative_base()


class Currency(Base):
    __tablename__ = 'currency'
    __table_args__ = {'sqlite_autoincrement': True}
    snowflake = Column(INTEGER, nullable=False)
    guild = Column(INTEGER, nullable=False)
    amount = Column(TEXT, nullable=False)
