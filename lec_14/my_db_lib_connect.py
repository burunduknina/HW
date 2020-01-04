import json
import pickle

import psycopg2
import redis
from pymongo import MongoClient


class MyMongo:

    def __init__(self, database, username, password, host, port):
        self.client = MongoClient(
            host=host, port=port, username=username, password=password)

    def set_value(self, obj, serializer, key, table, key_column, data_column,
                  database):
        data = dumps(obj, serializer)
        with self.client:
            db = self.client[database]
            db[table].insert_one({key_column: key, data_column: data})

    def get_value(
            self, key, serializer, table, key_column, data_column, database):
        with self.client:
            db = self.client[database]
            data = db[table].find_one({key_column: key})[data_column]
            return loads(data, serializer)


class MyRedis:

    def __init__(self, database, username, password, host, port):
        self.client = redis.Redis(
            host=host, port=port, db=database, password=password)

    def set_value(self, obj, serializer, key, table=None, key_column=None,
                  data_column=None, database=None):
        data = dumps(obj, serializer)
        self.client.set(key, data)

    def get_value(self, key, serializer, table=None, key_column=None,
                  data_column=None, database=None):
        data = self.client.get(key)
        return loads(data, serializer)


class MyPostgres:

    def __init__(self, database, username, password, host, port):
        self.client = psycopg2.connect(host=host, port=port, database=database,
                                       user=username, password=password)

    def set_value(self, obj, serializer, key, table, key_column, data_column,
                  database=None):
        data = dumps(obj, serializer)
        cur = self.client.cursor()
        cur.execute(f'INSERT INTO {table} ('
                    f'{key_column}, {data_column}) VALUES ('
                    f'%s, %s)',
                    (key, data,)
                    )
        self.client.commit()

    def get_value(self, key, serializer, table, key_column, data_column,
                  database=None):
        cur = self.client.cursor()
        cur.execute(
            f"SELECT {data_column} FROM "
            f"{table} WHERE {key_column} like '{key}';")
        result = cur.fetchone()
        data = result[0]
        return loads(data, serializer)


CLASSES = {'mongodb': MyMongo, 'redis': MyRedis, 'postgres': MyPostgres}


def dumps(data, serializer):
    if serializer == 'json':
        return json.dumps(data)
    elif serializer == 'pickle':
        return pickle.dumps(data)
    else:
        raise ValueError('Only json and pickle serializers are supported')


def loads(data, serializer):
    if serializer == 'json':
        return json.loads(data)
    elif serializer == 'pickle':
        return pickle.loads(data)
    else:
        raise ValueError('Only json and pickle serializers are supported')


def connect(db_type, database=0, username=None, password=None,
            host='127.0.0.1', port='0'):
    return CLASSES.get(db_type)(database, username, password, host, port)
