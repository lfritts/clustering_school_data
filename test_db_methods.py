import db_methods as dbm


def test_get_districts():
    district_list = dbm.get_districts()
    assert district_list[0] == "Aberdeen School District"
    assert district_list[-1] == "Zillah School District"


def test_get_schools():
    school_list = dbm.get_schools("Zillah School District")
    assert len(school_list) == 4
    assert school_list[0] == "Hilton Elementary School"
    assert school_list[3] == "Zillah Middle School"


def test_get_schools_by_id():
    school_ids = [1559, 5237, 4595]
    my_list = dbm.get_schools_by_id(school_ids)
    assert my_list[0][2] == "Lewis County Juvenile Detention"
    assert my_list[1][4] == 100
    assert my_list[2][3] == 899


def test_school_id():
    school_id = dbm.get_school_id("Jefferson Elementary",
                                  "Everett School District")
    assert school_id == 3533


def test_school_type():
    school_type = dbm.get_school_type(3533)
    assert school_type == "Elementary"