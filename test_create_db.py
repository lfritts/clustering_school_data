import create_db

def test_connect_db():
    con = create_db.connect_db()
    assert con is not None

def test_get_building_info():
    create_db.init_db()
    school = create_db.get_building_info(4005)
    assert school[0] == 4005
    assert school[1] == 62
