import psycopg2
from closest_schools import find_n_closest_schools as find_schools
from school_k import find_best_school_clusters
import os

DB_GET_DISTRICTS = """
SELECT DISTINCT district FROM demographics ORDER BY district;
"""

DB_GET_SCHOOLS = """
SELECT school, schooltype FROM demographics WHERE DISTRICT = %s
ORDER BY school;
"""

DB_GET_SCHOOLS_BY_TYPE = """
SELECT buildingid, {} FROM demographics WHERE schooltype = %s;
"""

DB_GET_SCHOOLS_BY_ID = """
SELECT  d.buildingid,
        d.district,
        d.school,
        d.enrollment,
        d.lowses,
        d.per_native,
        d.per_asian,
        d.per_PI,
        d.per_API,
        d.per_black,
        d.per_hispanic,
        d.per_migrant,
        d.per_bil,
        d.per_sped,
        y4.reading,
        y3.reading,
        y2.reading,
        y1.reading,
        y0.reading,
        y4.writing,
        y3.writing,
        y2.writing,
        y1.writing,
        y0.writing,
        y4.math,
        y3.math,
        y2.math,
        y1.math,
        y0.math,
        y4.science,
        y3.science,
        y2.science,
        y1.science,
        y0.science,
        y4.science
        FROM demographics d
        INNER JOIN year_0 y0
        ON d.buildingid = y0.buildingid AND y0.grade = %(grade)s
        INNER JOIN year_1 y1
        ON d.buildingid = y1.buildingid AND y1.grade = %(grade)s
        INNER JOIN year_2 y2
        ON d.buildingid = y2.buildingid AND y2.grade = %(grade)s
        INNER JOIN year_3 y3
        ON d.buildingid = y3.buildingid AND y3.grade = %(grade)s
        INNER JOIN year_4 y4
        ON d.buildingid = y4.buildingid AND y4.grade = %(grade)s
        WHERE d.buildingid IN %(id)s;
"""

DB_GET_READING_BY_ID = """
SELECT  d.school, y0.reading FROM demographics d INNER JOIN year_0 y0
        ON d.buildingid = y0.buildingid AND y0.grade = %(grade)s
        WHERE d.buildingid IN %(id)s;
"""

DB_GET_WRITING_BY_ID = """
SELECT  d.school, y0.writing FROM demographics d INNER JOIN year_0 y0
        ON d.buildingid = y0.buildingid AND y0.grade = %(grade)s
        WHERE d.buildingid IN %(id)s;
"""

DB_GET_MATH_BY_ID = """
SELECT  d.school, y0.math FROM demographics d INNER JOIN year_0 y0
        ON d.buildingid = y0.buildingid AND y0.grade = %(grade)s
        WHERE d.buildingid IN %(id)s;
"""

DB_GET_SCIENCE_BY_ID = """
SELECT  d.school, y0.science FROM demographics d INNER JOIN year_0 y0
        ON d.buildingid = y0.buildingid AND y0.grade = %(grade)s
        WHERE d.buildingid IN %(id)s;
"""

DB_GET_ID_FOR_SCHOOL = """
SELECT buildingid FROM demographics WHERE school = %s AND district = %s;
"""

DB_GET_TYPE_FOR_SCHOOL = """
SELECT schooltype FROM demographics where buildingid = %s;
"""

sub_keys = {
    "normalized_enrollment": "normalized_enrollment",
    "lowses": "lowses",
    "per_native": "per_native",
    "per_asian": "per_asian",
    "per_PI": "per_PI",
    "per_API": "per_API",
    "per_black": "per_black",
    "per_hispanic": "per_hispanic",
    "per_migrant": "per_migrant",
    "per_bil": "per_bil",
    "per_sped": "per_sped"
    }


def connect_db():
    host_name = os.environ.get('HOST', 'localhost')
    db_name = os.environ.get('DBNAME', 'schools_data')
    user_name = os.environ.get('USER', 'schools_admin')
    passwd = os.environ.get('PASSWORD', 'admin')
    conn_string = '''host={0} dbname={1} user={2} password={3}'''.format(
        host_name, db_name, user_name, passwd)
    con = psycopg2.connect('''{}'''.format(conn_string))
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


def get_schools_by_type(school_type, *args):
    cur = connect_db()
    sub_query = []
    print args
    for arg in args[0]:
        sub_query.append(sub_keys.get(arg, ""))
    sub_query = ", ".join(sub_query)
    query = DB_GET_SCHOOLS_BY_TYPE.format(sub_query)
    cur.execute(query, [school_type])
    return cur.fetchall()


def get_results(school_name, district, number_to_return, grade, *args):
    school_id = int(get_school_id(school_name, district))
    school_type = str(get_school_type(school_id))
    search_schools = get_schools_by_type(school_type, args[0])
    return_schools = find_schools(school_id, search_schools,
                                  int(number_to_return))
    schools = get_schools_by_id(grade, return_schools)
    target_school = get_schools_by_id(grade, school_id)
    return schools, target_school


def get_schools_by_id(grade, school_ids):
    if not isinstance(school_ids, list):
        temp = school_ids
        school_ids = []
        school_ids.append(temp)
    school_list = []
    cur = connect_db()
    cur.execute(DB_GET_SCHOOLS_BY_ID,
                {'grade': grade, 'id': tuple(school_ids)})
    school_list.append(cur.fetchall())
    return_list = make_dict(school_list[0], grade)
    return return_list


def make_dict(schools, grade):
    grade = int(grade)
    schools_dicts = []
    for item in schools:
        new_dict = {}
        new_dict['bid'] = item[0]
        new_dict['district'] = item[1]
        new_dict['school'] = item[2]
        demo = []
        for i in range(3, 14):
            demo.append(item[i])
        new_dict['demographics'] = demo
        scores = []
        for i in range(14, 19):
            scores.append(item[i])
        new_dict['reading'] = scores
        if grade == 4 or grade == 7 or grade == 10:
            scores = []
            for i in range(19, 24):
                scores.append(item[i])
            new_dict['writing'] = scores
        if grade <= 8:
            scores = []
            for i in range(24, 29):
                scores.append(item[i])
            new_dict['math'] = scores
        if grade == 5 or grade == 8:
            scores = []
            for i in range(29, 34):
                scores.append(item[i])
            new_dict['science'] = scores
        schools_dicts.append(new_dict)
    return schools_dicts


def get_scores_results(*args):
    if args[0] <= 5:
        school_type = 'Elementary'
    elif args[0] <= 8:
        school_type = 'Middle'
    else:
        school_type = 'High'
    search_schools = get_schools_by_type(school_type, args[2])
    demos, clusters = find_best_school_clusters(search_schools, K=4)
    keys = []
    demo0 = demos[0]
    demo1 = demos[1]
    demo2 = demos[2]
    demo3 = demos[3]
    cluster0 = clusters[0]
    cluster1 = clusters[1]
    cluster2 = clusters[2]
    cluster3 = clusters[3]
    for item in args[2]:
        keys.append(item)
    demo0 = list(zip(keys, demo0))
    demo1 = list(zip(keys, demo1))
    demo2 = list(zip(keys, demo2))
    demo3 = list(zip(keys, demo3))
    scores0 = get_scores_by_id(args[0], args[1], cluster0)
    scores1 = get_scores_by_id(args[0], args[1], cluster1)
    scores2 = get_scores_by_id(args[0], args[1], cluster2)
    scores3 = get_scores_by_id(args[0], args[1], cluster3)
    demos = []
    demos.append(demo0)
    demos.append(demo1)
    demos.append(demo2)
    demos.append(demo3)
    clusters = []
    clusters.append(cluster0)
    clusters.append(cluster1)
    clusters.append(cluster2)
    clusters.append(cluster3)
    return demos, clusters


def get_scores_by_id(grade, test, school_ids):
    if not isinstance(school_ids, list):
        temp = school_ids
        school_ids = []
        school_ids.append(temp)
    cur = connect_db()
    if test == 'reading':
        SQL_QUERY = DB_GET_READING_BY_ID
    elif test == 'writing':
        SQL_QUERY = DB_GET_WRITING_BY_ID
    elif test == "math":
        SQL_QUERY = DB_GET_MATH_BY_ID
    else:
        SQL_QUERY = DB_GET_SCIENCE_BY_ID
    cur.execute(SQL_QUERY, {'grade': grade, 'test': test,
                'id': tuple(school_ids)})
    school_list = cur.fetchall()
    return_list = [['School', 'Score']]
    for item in school_list:
        temp = [item[0], item[1]]
        return_list.append(temp)
    return clean_scores(return_list)


def clean_scores(return_list):
    for item in return_list[0]:
        if item[2] is None:
            return_list.pop(item)
