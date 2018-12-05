from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.services.database.models import Base, Prefix

engine = create_engine('sqlite:///event-bot.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


# If table doesn't exist, Create the database
if not engine.dialect.has_table(engine, 'prefix'):
    Base.metadata.create_all(engine)


def update_prefix(guild: int, prefix: str):
    if session.query(Prefix).filter(Prefix.guild == guild).count() > 0:
        Prefix.update(). \
            where(Prefix.guild == guild). \
            values(prefix=prefix)
    else:
        Prefix(guild=guild, prefix=prefix)
        session.add(Prefix)
    session.commit()
