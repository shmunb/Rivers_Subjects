from sqlalchemy import create_engine, text

water_type = {
    "река": 0,
    "море": 1,
    "озеро": 2,
    "водохранилище": 3}

water_type_inverted = {
    0: "река",
    1: "море",
    2: "озеро",
    3: "водохранилище"}

subject_type = {
    "область": 0,
    "край": 1,
    "ГФЗ": 2,
    "АО": 3,
    "республика": 4
}

subject_type_inverted = {
    0: "область",
    1: "край",
    2: "ГФЗ",
    3: "АО",
    4: "республика"
}


class DB(object):
    def __init__(self):
        self.engine = create_engine('sqlite:///data.db', echo=True)

    def drop_tables(self):
        print(self.engine.table_names())
        query_result = self.engine.execute('DELETE FROM waters')
        query_result = self.engine.execute('DELETE FROM subjects')

    def get_waters(self, order=None):

        query = ''

        if order is None:
            query = text('SELECT * FROM waters')
        else:
            query = text('SELECT * FROM waters ORDER BY ' + order)
        query_result = self.engine.execute(query)
        output = []
        for row in query_result:
            output.append(dict(row))
            output[len(output) - 1]['type'] = water_type_inverted[output[len(output) - 1]['type']]

        return output

    def get_subjects(self, order=None):

        query = ''

        if order is None:
            query = text('SELECT * FROM subjects')
        else:
            query = text('SELECT * FROM subjects ORDER BY ' + order)
        query_result = self.engine.execute(query)
        output = []
        for row in query_result:
            output.append(dict(row))
            output[len(output) - 1]['type'] = subject_type_inverted[output[len(output) - 1]['type']]

        return output

    def get_water_info(self, water_id):
        query = text('SELECT name, type, size FROM waters WHERE id =' + water_id)
        query_result = self.engine.execute(query)

        inflows = text('SELECT i.name AS into_, i.type AS type FROM waters f JOIN inflows inf JOIN waters i ON i.id = inf.id_into AND '
                       'f.id = inf.id_from WHERE inf.id_from = ' + str(water_id))
        inflows_result = self.engine.execute(inflows)

        inflows = []
        for i in inflows_result:
            inflows.append(i['into_'] + '(' + water_type_inverted[i['type']] + ')')

        inflows = ', '.join(inflows)
        print(inflows)

        output = []
        for row in query_result:
            res = dict(row)
            res['type'] = water_type_inverted[res['type']]
            if inflows != '':
                res['inflow'] = 'Впадает в:' + inflows
            else:
                res['inflow'] = ''
            output.append(res)

        return output[0]

    def get_subjects_for_water(self, water_id):
        query = text(
            'SELECT s.name as subject, s.type as type, s.id as id FROM subjects s JOIN waters_subjects ws JOIN waters '
            'w ON s.id = ws.id_subject AND w.id = ws.id_water WHERE ws.id_water =' + water_id)
        query_result = list(self.engine.execute(query))

        output = []
        for row in query_result:
            output.append(dict(row))
            output[len(output) - 1]['type'] = subject_type_inverted[output[len(output) - 1]['type']]

        return output

    def add_water(self, name, _type, size, inflow='NULL'):
        query = text('INSERT INTO waters VALUES (NULL, "' + str(name) + '", "' + str(_type) + '", "' + str(
            size) + str(inflow) + '")')
        query_result = self.engine.execute(query)

    def remove_water(self, name):
        query = text('DELETE FROM waters WHERE name = "' + name + '"')
        query_result = self.engine.execute(query)

    def add_subject_to_water(self, water_name, subject_name):
        query = text('INSERT INTO waters_subjects VALUES ((SELECT id FROM waters WHERE name = "' + str(
            water_name) + '"), (SELECT id FROM subjects WHERE name = "' + str(subject_name) + '"))')
        query_result = self.engine.execute(query)

    def remove_subject_from_water(self, subject_name):
        query = text(
            'DELETE FROM waters_subjects WHERE id_subject = (SELECT id FROM subjects WHERE name = "' + subject_name + '")')
        query_result = self.engine.execute(query)

    def add_subject(self, name, _type, size, population):
        query = text(
            'INSERT INTO subjects VALUES (NULL, "' + str(name) + '", "' + str(_type) + '", "' + str(size) + str(population) + '")')
        query_result = self.engine.execute(query)

    def remove_subject(self, name):
        query = text('DELETE FROM subjects WHERE name = "' + name + '"')
        query_result = self.engine.execute(query)
