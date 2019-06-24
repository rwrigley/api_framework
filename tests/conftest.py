import peewee
import pytest


@pytest.yield_fixture
def db():
    from playhouse.db_url import connect

    database = connect('sqlite:///:memory:')
    yield database
    if not database.is_closed():
        database.close()
