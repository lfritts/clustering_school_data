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
"""

DB_COPY_DATA = """
COPY demographics FROM %s;
"""

DB_GET_BUILDING = """
SELECT buildingid, enrollment, lowses FROM demographics WHERE buildingid
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
