import pytest
from db_fill import add_tea, fill_teas, INVALID_ARGS_TYPE_TEXT


class TestDatabase:
    def test_add_tea(self):
        with pytest.raises(TypeError) as exc_info:
            add_tea(name=1, grade='', region='', text='')
        assert INVALID_ARGS_TYPE_TEXT == str(exc_info.value)

    def test_fill_teas(self):
        with pytest.raises() as exc_info:
            fill_teas()
        assert 'error'


