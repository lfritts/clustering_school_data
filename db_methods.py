import psycopg2
from closest_schools import find_n_closest_schools as find_schools

DB_GET_DISTRICTS = """
SELECT DISTINCT district FROM demographics ORDER BY district;
"""

DB_GET_SCHOOLS = """
SELECT school FROM demographics WHERE DISTRICT = %s ORDER BY school;
"""

DB_GET_SCHOOLS_BY_TYPE = """
SELECT buildingid, per_black, per_hispanic FROM demographics
WHERE schooltype = %s;
"""

DB_GET_SCHOOLS_BY_TYPE_DEMO = """
SELECT {} FROM demographics
WHERE schooltype = %s;
"""


DB_GET_SCHOOLS_BY_ID = """
SELECT buildingid, district, school, enrollment, lowses FROM demographics
WHERE buildingid IN %s;
"""

DB_GET_ID_FOR_SCHOOL = """
SELECT buildingid FROM demographics WHERE school = %s AND district = %s;
"""

DB_GET_TYPE_FOR_SCHOOL = """
SELECT schooltype FROM demographics where buildingid = %s;
"""

sub_keys = {
    "enrollment": "enrollment",
    "lowses": "lowses",
    "per_black": "per_black"
    }


def connect_db():
    #user only has read access
    con = psycopg2.connect('''
        host=mpl-schoolappdata.ck0b6t86e1sf.us-west-2.rds.amazonaws.com
        dbname=school_data_2013 user=lfritts password=RRplxVG6Z6yCZYiaIwuiNO5Ik7gt0G''')
    return con.cursor()


def get_districts():
    cur = connect_db()
    cur.execute(DB_GET_DISTRICTS)
    districts = cur.fetchall()
    return [i[0] for i in districts]


def get_schools(district):
    cur = connect_db()
    cur.execute(DB_GET_SCHOOLS, [district])
    schools = cur.fetchall()
    return [i[0] for i in schools]


def get_school_id(school_name, district):
    cur = connect_db()
    cur.execute(DB_GET_ID_FOR_SCHOOL, [school_name, district])
    return cur.fetchone()[0]


def get_school_type(school_type):
    cur = connect_db()
    cur.execute(DB_GET_TYPE_FOR_SCHOOL, [school_type])
    return cur.fetchone()[0]

def get_schools_by_type_demo(school_type, *args):
    cur = connect_db()
    sub_query = []
    for arg in args[0]:
        sub_query.append(sub_keys.get(arg, ""))
    sub_query = ", ".join(sub_query)
    print "sub_query is: %s" % sub_query
    query = DB_GET_SCHOOLS_BY_TYPE_DEMO.format(sub_query)
    print "query is: {}\n".format(query)
    cur.execute(query, [school_type])
    return cur.fetchall()


def get_schools_by_type(school_type):
    cur = connect_db()
    cur.execute(DB_GET_SCHOOLS_BY_TYPE, [school_type])
    return cur.fetchall()

def get_results(school_name, district, number_to_return, *args):
# def get_results(school_name, district, number_to_return):
    school_id = int(get_school_id(school_name, district))
    school_type = str(get_school_type(school_id))
    # search_schools = get_schools_by_type(school_type)
    search_schools = get_schools_by_type_demo(school_type, args)
    print school_id in search_schools[:][0]
    return_schools = find_schools(school_id, search_schools,
                                  int(number_to_return))
    return get_schools_by_id(return_schools)


def get_schools_by_id(school_ids):
    school_list = []
    cur = connect_db()
    cur.execute(DB_GET_SCHOOLS_BY_ID, [tuple(school_ids)])
    school_list.append(cur.fetchall())
    return school_list[0]
