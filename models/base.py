from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from .engine import engine


class Base:
    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    id = Column(Integer, primary_key=True, autoincrement=True)


Base = declarative_base(bind=engine, cls=Base)
