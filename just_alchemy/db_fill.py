from models import Session, Tea, Comment, User, Base, engine
import sqlalchemy.exc

INVALID_ARGS_TYPE_TEXT = 'all args have to be str'


def try_session_commit():
    try:
        Session.commit()
    except Exception as e:
        raise e


def add_tea(name, grade, region, text):
    if not all(map(
            lambda v: isinstance(v, (str,)),
            (name, grade, region, text),
    )):
        raise TypeError(INVALID_ARGS_TYPE_TEXT)

    preview = text[0:100] if len(text) > 100 else text

    tea = Tea(name=name, grade=grade, region=region, text=text, preview=preview)
    Session.add(tea)
    try_session_commit()


def add_user(name, mail):
    user = User(name=name, mail=mail, password='12345')
    Session.add(user)
    try_session_commit()


def add_comment(user, tea, text):
    comment = Comment(user_id=user.id, tea_id=tea.id, text=text)
    Session.add(comment)
    try_session_commit()


def check_exist(class_name):
    class_objects = []
    try:
        class_objects = Session.query(class_name).all()
    except sqlalchemy.exc.OperationalError as e:
        Base.metadata.create_all(engine)
        print(f'{e}\nTables created.')

    if len(class_objects) == 0:
        return False
    else:
        return True


def fill_teas():
    if not check_exist(Tea):
        texts = ('''Да Хун Пао(大红袍, Da Hong Pao, Большой Красный Халат, ДХП, Дахунпао) – это китайский чай,
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
                Халатом кусты чая.Так и появилось название Да Хун Пао: «Большой красный халат».''',
                 'NULL',
                 'NULL',
                 'NULL'
                 )
        names = ('Да Хун Пао', 'Те Гуань Инь', 'Сяо Чжун', 'ГАБА')
        grades = ('Темный Улун', 'Светлый Улун', 'Красный', 'Светлый Улун')
        regions = ('УиШань', 'ФуЦзянь', 'УиШань', 'Тайвань')
        for num, name in enumerate(names):
            add_tea(name=name, grade=grades[num], region=regions[num], text=texts[num])

        try_session_commit()


def fill_users():
    if not check_exist(User):
        name, mail = 'samplename', 'samplemail@web.com'
        add_user(name, mail)
        name, mail = 'samplename_2', 'samplemail_2@web.com'
        add_user(name, mail)


def fill_comments():
    if not check_exist(Comment):
        tea = Session.query(Tea).first()
        users = Session.query(User).all()
        text = 'good'
        for user in users:
            add_comment(user, tea, text)
            text = 'bad'


def fill_db():
    fill_teas()
    fill_users()
    fill_comments()
