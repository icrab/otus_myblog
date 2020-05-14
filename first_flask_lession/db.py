import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text,\
                        ForeignKey, DateTime
from sqlalchemy.orm import Session, relationship

engine = create_engine('sqlite:///base.db')
Base = declarative_base()
session = Session(engine)


class Tea(Base):
    __tablename__ = 'teas'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    grade = Column(String, nullable=False)
    region = Column(String, nullable=False)
    img = Column(String, nullable=False, default='img/dhp.jpg')

    comment = relationship('Comment', back_populates='tea')
    post = relationship('Post', back_populates='tea')

    def __repr__(self):
        return f'<Tea: #{self.id} {self.name}: {self.grade}, {self.region}>'


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
        return f'<Comment: #{self.id}, user {self.user.name} about {self.tea.name}:{self.text} {self.datetime}>'


def add_tea(name, grade, region):
    tea = Tea(name=name, grade=grade, region=region)
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


def add_user(name, mail):
    user = User(name=name, mail=mail)
    session.add(user)
    session.flush(session)


def add_comment(user, tea, text):
    comment = Comment(user_id=user.id, tea_id=tea.id, text=text)
    session.add(comment)


def check_exist(class_name):
    class_objects = session.query(class_name).all()
    if len(class_objects) == 0:
        return False
    else:
        return True


def db_fill():
    if not check_exist(Tea):
        name, grade, region = 'Да Хун Пао', 'Темный Улун', 'Уишань'
        add_tea(name, grade, region)
        name, grade, region = 'Те Гуань Инь', 'Светлый Улун', 'Фуцзянь'
        add_tea(name, grade, region)

    tea = session.query(Tea).filter_by(name='Да Хун Пао').first()
    if not check_exist(Post):
        add_post(tea)

    if not check_exist(User):
        name, mail = 'samplename', 'samplemail@web.com'
        add_user(name, mail)
        name, mail = 'samplename_2', 'samplemail_2@web.com'
        add_user(name, mail)
    users = session.query(User).all()

    if not check_exist(Comment):
        text = 'good'
        for user in users:
            add_comment(user, tea, text)
            text = 'bad'

    session.commit()


def main():
    Base.metadata.create_all(engine)
    db_fill()

    tea = session.query(Tea).first()
    post = session.query(Post).filter_by(tea_id=tea.id).first()

    print(f'{tea}\n{post.text}')


if __name__ == '__main__':
    main()
