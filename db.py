from sqlalchemy import create_engine, text


class DB(object):
    def __init__(self):
        self.engine = create_engine('sqlite:///data.db', echo=True)




    def get_waters(self):
        query = text('SELECT * FROM waters')
        query_result = self.engine.execute(query)

        output = []
        for row in query_result:
            output.append(dict(row))

        return output

    def get_subjects(self):
        query = text('SELECT * FROM subjects')
        query_result = self.engine.execute(query)

        output = []
        for row in query_result:
            output.append(dict(row))

        return output

    def get_water_info(self, water_id):
        query = text('SELECT name, type, size FROM waters WHERE id =' + water_id)
        query_result = self.engine.execute(query)

        output = []
        for row in query_result:
            output.append(dict(row))

        return output[0]

    def get_subjects_for_water(self, water_id):
        query = text(
            'SELECT e.name AS subject, type, size, population FROM subjects e JOIN waters_subjects me JOIN waters m ON e.id = me.id_subject AND m.id = me.id_water WHERE me.id_water =' + water_id)
        query_result = self.engine.execute(query)

        output = []
        for row in query_result:
            output.append(dict(row))

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
