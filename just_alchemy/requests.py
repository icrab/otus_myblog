from models import Session, Tea, User


def get_users():
    users = Session.query(User).all()
    print(f'Users:\n{users}')

    Session.close()


def get_teas():
    teas = Session.query(Tea).all()
    print(f'Teas:\n{teas}')

    Session.close()


def get_users_with_comments():
    users_with_comments = Session.query(User).filter(User.comment!=None).all()
    print('Users with comments:')
    for user in users_with_comments:
        print(f'User {user.name} write comment {user.comment}')

    Session.close()


if __name__ == '__main__':
    get_users()
    get_teas()
    get_users_with_comments()

