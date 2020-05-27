import psycopg2

from src import parameter_fetcher


class RedshiftConnector:
    def __init__(self, env: str = 'default'):
        self.pf = parameter_fetcher.ParameterFetcher(env)

    def do_query(self, query):
        fetch_all = []
        cursor = self.get_cursor()
        cursor.execute(query)
        fetch_all.append(cursor.fetchall())
        cursor.close()
        return fetch_all

    def get_connect_info(self, host, port, user, database, password):
        return {
            "host": self.parameter_fetcher.fetch_parameters(host),
            "port": self.parameter_fetcher.fetch_parameters(port),
            "user": self.parameter_fetcher.fetch_parameters(user),
            "database": self.parameter_fetcher.fetch_parameters(database),
            "password": self.parameter_fetcher.fetch_parameters(password)
        }

    def connect(self):
        return psycopg2.connect(**self.get_connect_info())

    def get_cursor(self):
        return self.connect().cursor()
