import pytest
from models_import import User, Tea, Comment, Session
from requests import FAILED_USER_REMOVE, remove_user
from db_fill import add_tea, fill_teas, fill_users, fill_comments, INVALID_ARGS_TYPE_TEXT


class TestDatabase:
    def test_add_single_tea(self):
        with pytest.raises(TypeError) as exc_info:
            add_tea(name=1, grade='', region='', text='')
        assert INVALID_ARGS_TYPE_TEXT == str(exc_info.value)

    def test_fill_teas(self):
        fill_teas()
        teas = Session.query(Tea).all()
        Session.close()
        assert len(teas) == 4

    def test_fill_users(self):
        fill_users()
        users = Session.query(User).all()
        Session.close()
        assert len(users) == 2

    def test_fill_comments(self):
        fill_comments()
        comments = Session.query(Comment).all()
        Session.close()
        assert len(comments) == 2

    def test_remove_user_with_comment(self):
        user = Session.query(User).filter(User.comment!=None).first()
        Session.close()
        with pytest.raises(RuntimeError) as exc_info:
            remove_user(user)
        assert FAILED_USER_REMOVE == str(exc_info.value)



