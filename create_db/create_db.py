# -*- coding: utf-8 -*-

from contextlib import closing
import os
import psycopg2

# database constructs
DB_SCHEMA = """
DROP TABLE IF EXISTS demographics;
CREATE TABLE demographics (
    buildingid INTEGER UNIQUE PRIMARY KEY,
    schooltype TEXT NOT NULL,
    district TEXT NOT NULL,
    school TEXT NOT NULL,
    enrollment INTEGER NOT NULL,
    lowses REAL NOT NULL,
    normalized_enrollment REAL NOT NULL
);
"""

DB_COPY_DATA = """
COPY demographics FROM %s;
"""

DB_GET_BUILDING = """
SELECT buildingid, enrollment, lowses FROM demographics WHERE buildingid
= %s;
"""

def connect_db():
    return psycopg2.connect(database="postgres")

def init_db():
    with closing(connect_db()) as db:
        db.cursor().execute(DB_SCHEMA)
        db.commit()
        db.cursor().execute(DB_COPY_DATA, [os.getcwd() +
                            "/demographics_data.txt"])
        db.commit()

def get_building_info(building_id):
    con = connect_db()
    cur = con.cursor()
    cur.execute(DB_GET_BUILDING, [building_id])
    return cur.fetchone()
