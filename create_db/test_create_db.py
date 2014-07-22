import create_db
import pytest


def test_connect_db():
    con = create_db.connect_db()
    assert con is not None

def test_get_building_info():
    create_db.init_db()
    school = create_db.get_building_info(4005)
    assert school[0] == 4005
    assert school[1] == 62

def test_year_0_db():
    create_db.init_db()
    data = create_db.get_data(year_0, 4005)
    return_list = [7, 65.5, 41.4, 36.7, 'NA', 8, 54.1, 24.3, 'NA', 37.8]
    assert data == return_list
