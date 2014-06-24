import db_methods as dbm


def test_get_districts():
    district_list = dbm.get_districts()
    assert district_list[0][0] == "Aberdeen School District"
    assert district_list[-1][0] == "Zillah School District"


def test_get_schools():
    school_list = dbm.get_schools("Zillah School District")
    assert len(school_list) == 4
    assert school_list[0][0] == 2783
    assert school_list[3][1] == "Zillah Middle School"

def test_get_schools_by_id():
    school_ids = [1559, 5237, 4595]
    my_list = dbm.get_schools_by_id(school_ids)
    assert my_list[0][1] == "Lewis County Juvenile Detention"
    assert my_list[1][3] == 100
    assert my_list[2][2] == 899

def get_schools_for_cluster():
    #what is the name of the function to call
    pass