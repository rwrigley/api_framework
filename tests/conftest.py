import peewee
import pytest
import falcon
from falcon import testing
from .models import proxy


@pytest.yield_fixture
def db():
    from playhouse.db_url import connect

    database = connect('sqlite:///:memory:')
    yield database
    if not database.is_closed():
        database.close()

@pytest.yield_fixture
def bind_models(db):
    def bind(*models):
        proxy.initialize(db)
        db.create_tables(models)
    return bind

@pytest.yield_fixture
def build_test_client(db):
    def build(controllers):
        api = falcon.API()

        for route, controller in controllers.items():
            api.add_route(route, controller)

        return testing.TestClient(api)
    return build

