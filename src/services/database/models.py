from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import DATETIME, INTEGER, TEXT

Base = declarative_base()


class Prefix(Base):
    __tablename__ = 'prefix'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(INTEGER, primary_key=True, nullable=False)
    guild = Column(TEXT)
    prefix = Column(TEXT)
