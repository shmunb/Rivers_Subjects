from sqlalchemy import create_engine, text


class DB(object):
    def __init__(self):
        self.engine = create_engine('sqlite:///data.db', echo=True)

    def get_waters(self):
        query = text('SELECT * FROM rivers')
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

