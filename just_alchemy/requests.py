from models import Session, Tea, User
import sqlalchemy.exc


FAILED_USER_REMOVE = 'Remove Failed. This user have a comment'


def get_users():
    users = Session.query(User).all()
    Session.close()
    return users


def get_teas():
    teas = Session.query(Tea).all()
    Session.close()
    return teas


def get_users_with_comments():
    users_with_comments = Session.query(User).filter(User.comment!=None).all()
    Session.close()
    return users_with_comments


def remove_user(user):
    try:
        Session.delete(user)
        Session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise RuntimeError(FAILED_USER_REMOVE)
