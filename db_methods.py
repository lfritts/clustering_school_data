
import psycopg2
from closest_schools import find_n_closest_schools as find_schools

DB_GET_DISTRICTS = """
SELECT DISTINCT district FROM demographics ORDER BY district;
"""

# DB_GET_SCHOOLS = """
# SELECT school FROM demographics WHERE district = %s ORDER BY school;
# """

DB_GET_SCHOOLS = """
SELECT school FROM demographics ORDER BY school;
"""

DB_GET_SCHOOLS_BY_TYPE = """
SELECT buildingid, enrollment, lowses FROM demographics WHERE
schooltype = %s;
"""

DB_GET_SCHOOLS_BY_ID = """
SELECT buildingid, district, school, enrollment, lowses FROM demographics
WHERE buildingid = %s;
"""

DB_GET_ID_FOR_SCHOOL = """
SELECT buildingid FROM demographics WHERE school = %s;
"""

def connect_db():
    con = psycopg2.connect('''
        host=w2-schoolwebapp.cp9cgekjzx3g.us-west-2.rds.amazonaws.com
        dbname=school_data_2013 user=lfritts
        password=''')
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


def get_similar_schools(school_id, school_type, num2return):
    cur = connect_db()
    cur.execute(DB_GET_SCHOOLS_BY_TYPE, [school_type])
    return get_schools_by_id(find_schools(school_id, cur.fetchall(),
                             num2return))

def get_id_for_selected_school(school_id):
    cur = connect_db()
    return cur.execute(DB_GET_ID_FOR_SCHOOL, [school_id])


def get_schools_by_id(school_ids):
    school_list = []
    cur = connect_db()
    for sid in school_ids:
        cur.execute(DB_GET_SCHOOLS_BY_ID, [sid])
        school_list.append(cur.fetchone())
    return school_list
