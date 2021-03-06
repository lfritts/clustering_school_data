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


def test_school_id():
    school_id = dbm.get_school_id("Jefferson Elementary",
                                  "Everett School District")
    assert school_id == 3533


def test_school_type():
    school_type = dbm.get_school_type(3533)
    assert school_type == "Elementary"

def test_schools_by_id():
    school_ids = [2824, 2890, 2530, 4149]
    return_list = dbm.get_schools_by_id(school_ids)
    assert len(return_list) == 4

def test_get_results():
    the_list = dbm.get_results("Chiawana High School", "Pasco School District",
                               20, "normalized_enrollment", "lowses", "per_black")
    print the_list
