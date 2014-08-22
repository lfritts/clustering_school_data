import os
from contextlib import closing
import pytest
import create_db


TEST_DSN = 'dbname=test_schools_data'


@pytest.fixture(scope='session')
def test_app():
    os.environ['TEST_DB'] = TEST_DSN


def clear_db():
    with closing(create_db.connect_db()) as db:
        db.cursor().execute("DROP TABLE entries")
        db.commit()


@pytest.fixture(scope='session')
def db(test_app, request):
    create_db.init_db()

    def cleanup():
        clear_db()
    request.addfinalizer(cleanup)


def test_connect_db():
    con = create_db.connect_db()
    assert con is not None


def test_get_building_info():
    school = create_db.get_building_info(4005)
    assert school[0] == 4005
    assert school[1] == 62


def test_year_0_db():
    data = create_db.get_data(4005)
    return_list = (7, 65.5, 41.4, 36.7, None)
    assert data == return_list
