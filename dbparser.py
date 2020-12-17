from db import *
import sys
import os

waters = "./водоёмы.txt"
subjects = "./субъекты.txt"
w_s = "./в-с.txt"
inflows = "впадения.txt"

def run_base(db):
    # db.engine.execute('.mode columns')
    # db.engine.execute('.headers on')
    # db.engine.execute('.schema foreign_keys = on;')
    db.engine.execute('CREATE TABLE waters(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, '
                      'type INTEGER, size INTEGER NOT NULL);')
    db.engine.execute('CREATE TABLE subjects(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, '
                      'type INTEGER, size INTEGER NOT NULL, population INTEGER NOT NULL);')
    db.engine.execute('CREATE TABLE waters_subjects(id_water INTEGER NOT NULL, id_subject INTEGER NOT NULL, '
                      'PRIMARY KEY(id_water, id_subject), FOREIGN KEY (id_water) REFERENCES waters(id), FOREIGN KEY ('
                      'id_subject) REFERENCES subjects(id));')

    db.engine.execute('CREATE TABLE inflows(id_from INTEGER NOT NULL, id_into INTEGER NOT NULL, PRIMARY KEY(id_from, '
                      'id_into), FOREIGN KEY (id_from) REFERENCES waters(id), FOREIGN KEY (id_into) REFERENCES'
                      ' waters(id));')


def parse_waters(db):

    fw = open(waters, 'r', encoding='utf-8')
    line = fw.readline()

    while line:
        obj = line.split(' ')
        query = text('INSERT INTO waters VALUES (NULL, "' + obj[1] + '", "' + obj[2] + '", "' + obj[3] +  '")')
        query_result = db.engine.execute(query)
        line = fw.readline()

    fw.close()


def parse_subjects(db):

    fs = open(subjects, 'r', encoding='utf-8')
    line = fs.readline()

    while line:
        obj = line.split(' ')
        query = text('INSERT INTO subjects VALUES (NULL, "' + obj[1] + '", "' + obj[2] + '", "' + obj[3] + '", "' + obj[4] + '")')
        query_result = db.engine.execute(query)
        line = fs.readline()

    fs.close()


def parse_inflows(db):
    fs = open(inflows, 'r')
    line = fs.readline()

    while line:
        obj = line.split(' ')
        query = text('INSERT INTO inflows VALUES ("' + obj[0] + '", "' + obj[1] + '")')
        query_result = db.engine.execute(query)
        line = fs.readline()

    fs.close()

def parse_relations(db):
    fs = open(w_s, 'r')
    line = fs.readline()

    while line:
        obj = line.split(' ')
        query = text('INSERT INTO waters_subjects VALUES ("' + obj[0] + '", "' + obj[1] + '")')
        query_result = db.engine.execute(query)
        line = fs.readline()

    fs.close()