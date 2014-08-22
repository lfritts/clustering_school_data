# -*- coding: utf-8 -*-

from contextlib import closing
import os
import psycopg2

# database constructs:
# the database consists of several tables that all have a building id in
# common.  The tables will be joined based on that id for the results.
DB_SCHEMA = """
DROP TABLE IF EXISTS demographics;
CREATE TABLE demographics (
    buildingid INTEGER,
    schooltype TEXT NOT NULL,
    district TEXT NOT NULL,
    school TEXT NOT NULL,
    enrollment INTEGER NOT NULL,
    lowses REAL NOT NULL,
    normalized_enrollment REAL NOT NULL,
    per_native REAL NOT NULL,
    per_asian REAL NOT NULL,
    per_PI REAL NOT NULL,
    per_API REAL NOT NULL,
    per_black REAL NOT NULL,
    per_hispanic REAL NOT NULL,
    per_migrant REAL NOT NULL,
    per_bil REAL NOT NULL,
    per_sped REAL NOT NULL
);
DROP TABLE IF EXISTS year_0;
CREATE TABLE year_0 (
    buildingid INTEGER,
    grade INTEGER,
    reading REAL,
    math REAL,
    writing REAL,
    science REAL
    );
DROP TABLE IF EXISTS year_1;
CREATE TABLE year_1 (
    buildingid INTEGER,
    grade INTEGER,
    reading REAL,
    math REAL,
    writing REAL,
    science REAL
    );
DROP TABLE IF EXISTS year_2;
CREATE TABLE year_2 (
    buildingid INTEGER,
    grade INTEGER,
    reading REAL,
    math REAL,
    writing REAL,
    science REAL
    );
DROP TABLE IF EXISTS year_3;
CREATE TABLE year_3 (
    buildingid INTEGER,
    grade INTEGER,
    reading REAL,
    math REAL,
    writing REAL,
    science REAL
    );
DROP TABLE IF EXISTS year_4;
CREATE TABLE year_4 (
    buildingid INTEGER,
    grade INTEGER,
    reading REAL,
    math REAL,
    writing REAL,
    science REAL
    );
"""

# For testing
DB_COPY_DATA = """
COPY %s FROM %s DELIMITER E'\t' CSV HEADER;
"""

DB_GET_BUILDING = """
SELECT buildingid, enrollment, lowses FROM demographics WHERE buildingid
= %s;
"""

DB_GET_DATA = """
SELECT grade, reading, math, writing, science FROM year_0 WHERE buildingid
= %s;
"""


def connect_db():

    if 'RDS_HOSTNAME' in os.environ:
        DATABASES = {
            'default': {
                'ENGINE': 'postgres (9.3.3) ',
                'NAME': os.environ['RDS_DB_NAME'],
                'USER': os.environ['RDS_USERNAME'],
                'PASSWORD': os.environ['RDS_PASSWORD'],
                'HOST': os.environ['RDS_HOSTNAME'],
                'PORT': os.environ['RDS_PORT'],
            }
        }
        return psycopg2.connect(DATABASES)
    else:
        print "Hello"
        conn_string = "host='localhost' dbname='schools_data' user='schools_admin' password='admin'"
    return psycopg2.connect(conn_string)


def init_db():
    with closing(connect_db()) as db:
        db.cursor().execute(DB_SCHEMA)
        db.commit()
        db.cursor().execute(DB_COPY_DATA, "demographics", [os.getcwd() +
                            "/demographics.txt"])
        db.cursor().execute(DB_COPY_DATA, "year_0", [os.getcwd() +
                            "/year_0"])
        db.commit()


def get_building_info(building_id):
    con = connect_db()
    cur = con.cursor()
    cur.execute(DB_GET_BUILDING, [building_id])
    return cur.fetchone()
