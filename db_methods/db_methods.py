
import psycopg2
#from school_k import find_schools_in_cluster as cluster

DB_GET_DISTRICTS = """
SELECT DISTINCT district FROM demographics ORDER BY district;
"""

DB_GET_SCHOOLS = """
SELECT buildingid, school FROM demographics WHERE district = %s ORDER BY
school;
"""

DB_GET_SCHOOLS_BY_TYPE = """
SELECT buildingid, enrollment, lowses FROM demographics WHERE
schooltype = %s;
"""

DB_GET_SCHOOLS_BY_ID = """
SELECT district, school, enrollment, lowses FROM demographics WHERE
buildingid = %s;
"""


def connect_db():
    con = psycopg2.connect('''
        host=w2-schoolwebapp.cp9cgekjzx3g.us-west-2.rds.amazonaws.com
        dbname=school_data_2013 user=lfritts
        password=year2k13:DB:Xl9ux!Y%3v''')
    return con.cursor()


def get_districts():
    cur = connect_db()
    cur.execute(DB_GET_DISTRICTS)
    return cur.fetchall()


def get_schools(district):
    cur = connect_db()
    cur.execute(DB_GET_SCHOOLS, [district])
    return cur.fetchall()


def get_schools_for_cluster(school_id, school_type):
    cur = connect_db()
    cur.execute(DB_GET_SCHOOLS_BY_ID, [school_type])
    return get_schools_by_id(cluster(school_id, cur.fetchall()))


def get_schools_by_id(school_ids):
    school_list = []
    cur = connect_db()
    for sid in school_ids:
        cur.execute(DB_GET_SCHOOLS_BY_ID, [sid])
        school_list.append(cur.fetchone())
    return school_list
