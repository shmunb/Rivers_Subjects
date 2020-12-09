from db import *
import sys
import os

waters = "./водоёмы.txt"
subjects = "./субъекты.txt"


def parse_waters(db):

    fw = open(waters, 'r')
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

    fs = open(subjects, 'r')
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
        query = text('INSERT INTO subjects VALUES (NULL, "' + obj[0] + '", "' + obj[1])
        query_result = db.engine.execute(query)
        line = fs.readline()

    fs.close()