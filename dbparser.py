from db import *
import sys
import os

waters = "./водоёмы.txt"
subjects = "./субъекты.txt"

def run_base(db):
    # db.engine.execute('.mode columns')
    # db.engine.execute('.headers on')
    # db.engine.execute('.schema foreign_keys = on;')
    db.engine.execute('CREATE TABLE waters(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, type INTEGER, size INTEGER NOT NULL, inflow INTEGER NOT NULL);')
    db.engine.execute('CREATE TABLE subjects(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, type INTEGER, size INTEGER NOT NULL, population INTEGER NOT NULL);')
    db.engine.execute('CREATE TABLE waters_subjects(id_water INTEGER NOT NULL, id_subject INTEGER NOT NULL, PRIMARY KEY(id_water, id_subject), FOREIGN KEY (id_water) REFERENCES waters(id), FOREIGN KEY (id_subject) REFERENCES subjects(id));')

def parse_waters(db):

    fw = open(waters, 'r', encoding='utf-8')
    line = fw.readline()

    while line:
        obj = line.split(' ')
        if obj[2] != '0':
            obj.append('NULL')
        query = text('INSERT INTO waters VALUES (NULL, "' + obj[1] + '", "' + obj[2] + '", "' + obj[3] + '", "' + obj[4] + '")')
        query_result = db.engine.execute(query)
        line = fw.readline()

    fw.close()


def parse_subjects(db):

    fs = open(subjects, 'r', encoding='utf-8')
    line = fs.readline()

    while line:
        obj = line.split(' ')
        if obj[2] != '0':
            obj.append('NULL')
        query = text('INSERT INTO subjects VALUES (NULL, "' + obj[1] + '", "' + obj[2] + '", "' + obj[3] + '", "' + obj[4] + '")')
        query_result = db.engine.execute(query)
        line = fs.readline()

    fs.close()


def parse_relations(db):
    fs = open(subjects, 'r')
    line = fs.readline()

    while line:
        obj = line.split(' ')
        query = text('INSERT INTO subjects VALUES (NULL, "' + obj[0] + '", "' + obj[1] + '")')
        query_result = db.engine.execute(query)
        line = fs.readline()

    fs.close()