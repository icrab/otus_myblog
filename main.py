import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text,\
                        ForeignKey, DateTime
from sqlalchemy.orm import Session, relationship

engine = create_engine('sqlite:///base.db')
Base = declarative_base()
session = Session(engine)


class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    region = Column(String, nullable=False)

    tea = relationship('Tea', back_populates='grade')

    def __repr__(self):
        return f'<Grade: #{self.id} {self.name}, {self.region}>'


class Tea(Base):
    __tablename__ = 'teas'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    grade_id = Column(Integer, ForeignKey(Grade.id), nullable=False)

    grade = relationship('Grade', back_populates='tea')
    comment = relationship('Comment', back_populates='tea')
    post = relationship('Post', back_populates='tea')

    def __repr__(self):
        return f'<Tea: #{self.id} {self.name}>'


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    tea_id = Column(Integer, ForeignKey(Tea.id))
    text = Column(Text)
    preview = Column(Text)

    tea = relationship('Tea', back_populates='post')

    def __repr__(self):
        return f'<Post: #{self.id} {self.tea_id} {self.text}>'

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    mail = Column(String, nullable=False)

    comment = relationship('Comment', back_populates='user')

    def __repr__(self):
        return f'<User: #{self.id} {self.name}>'


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    tea_id = Column(Integer, ForeignKey(Tea.id), nullable=False)
    text = Column(Text, nullable=False)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship('User', back_populates='comment')
    tea = relationship('Tea', back_populates='comment')

    def __repr__(self):
        return f'<Comment: #{self.id} {self.text} {self.datetime}>'


def add_grade():
    grade = Grade(name='Темный Улун', region='Уишань')
    session.add(grade)
    session.flush(session)


def add_tea(grade):
    tea = Tea(name='Да Хун Пао', grade_id=grade.id)
    session.add(tea)
    session.flush(session)


def add_post(tea):
    text = '''Да Хун Пао(大红袍, Da Hong Pao, Большой Красный Халат, ДХП, Дахунпао) – это китайский чай,
    который производят на северо - западе провинции Фуцзянь, в горах Уи.По классу его относят к
    улунам сильной ферментации. Да Хун Пао – один из самых известных сортов китайского
    чая, наряду с такими, как Пуэр, Те Гуань Инь, Лун Цзин. Но по количеству легенд и мифов, Красный
    Халат, пожалуй, на первом месте. Как гласят исторические записи монастыря Тян Син Сы, в 1385 г.в
    династию Мин(в 18 год под девизом Хун У), студент Дин Сянь, направляясь на сдачу императорских
    экзаменов, получил тепловой удар, и один из монахов вышеназванного монастыря использовал чай,
    чтобы его вылечить. Успешно сдав экзамен и получив высокую должность Чжуан Юань
    (которой соответствовал большой красный халат с изображением драконов), желая отблагодарить Будду
    за чудесное излечение, Дин Сянь вернулся в монастырь, где преподнес Халат монаху, который его
    излечил.Но монах, как истинный буддист, не принял столь высокий дар. Тогда чиновник укрыл
    Халатом кусты чая.Так и появилось название Да Хун Пао: «Большой красный халат».
    '''
    post = Post(tea_id=tea.id, text=text, preview='DAAH')
    session.add(post)


def add_user():
    user = User(name='asd', mail='asd@mail.ru')
    session.add(user)
    session.flush(session)


def add_comment(user, tea):
    comment = Comment(user_id=user.id, tea_id=tea.id, text='my first comment')
    session.add(comment)


def main():
    Base.metadata.create_all(engine)

    grades = session.query(Grade).all()
    if len(grades) == 0:
        add_grade()
    grade = session.query(Grade).first()

    teas = session.query(Tea).all()
    if len(teas) == 0:
        add_tea(grade)
    tea = session.query(Tea).first()

    posts = session.query(Post).all()
    if len(posts) == 0:
        add_post(tea)

    add_user()
    user = session.query(User).first()
    add_comment(user, tea)
    session.commit()
    post = session.query(Post).first()
    tea = session.query(Tea).filter_by(id=post.tea_id).first()
    grade = session.query(Grade).filter_by(id=tea.grade_id).first()
    print(f'{tea}\n{grade}\n{post.text}')


if __name__ == '__main__':
    main()
