import datetime
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import Column, Integer, String, Text, \
                       ForeignKey, DateTime
from .engine import engine
from .base import Base


session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class Tea(Base):
    name = Column(String, nullable=False, unique=True)
    grade = Column(String, nullable=False)
    region = Column(String, nullable=False)
    img = Column(String, nullable=False, default='dhp.jpg')
    text = Column(Text)
    preview = Column(Text)

    comment = relationship('Comment', back_populates='tea')

    def __repr__(self):
        return f'<Tea: #{self.id} {self.name}: {self.grade}, {self.region}>'


class User(Base):
    name = Column(String, nullable=False)
    mail = Column(String, nullable=False)
    password = Column(String, nullable=False)
    registration_time = Column(DateTime, default=datetime.datetime.utcnow)

    comment = relationship('Comment', back_populates='user')

    def __repr__(self):
        return f'{self.name}'


class Comment(Base):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    tea_id = Column(Integer, ForeignKey(Tea.id), nullable=False)
    text = Column(Text, nullable=False)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship('User', back_populates='comment')
    tea = relationship('Tea', back_populates='comment')

    def __repr__(self):
        return f'<Comment: #{self.id}, about {self.tea.name}:{self.text} {self.datetime}>'


