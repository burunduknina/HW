import json
import pickle

import psycopg2
import redis
from pymongo import MongoClient


class MyMongo:
    @staticmethod
    def set_value(data, key, table, key_column, data_column, database,
                  username, password, host, port):
        client = MongoClient(
            host=host, port=port, username=username, password=password)
        with client:
            db = client[database]
            db[table].insert_one({key_column: key, data_column: data})

    @staticmethod
    def get_value(key, table, key_column, data_column, database, username,
                  password, host, port):
        client = MongoClient(host=host, port=port, authSource=database,
                             username=username, password=password)
        with client:
            db = client[database]
            return db[table].find_one({key_column: key})[data_column]


class MyRedis:
    @staticmethod
    def set_value(data, key, table, key_column, data_column, database,
                  username, password, host, port):
        client = redis.Redis(
            host=host, port=port, db=database, password=password)
        client.set(key, data)

    @staticmethod
    def get_value(key, table, key_column, data_column, database, username,
                  password, host, port):
        client = redis.Redis(
            host=host, port=port, db=database, password=password)
        return client.get(key)


class MyPostgres:
    @staticmethod
    def set_value(data, key, table, key_column, data_column, database,
                  username, password, host, port):
        client = psycopg2.connect(host=host, port=port, database=database,
                                  user=username, password=password)
        cur = client.cursor()
        cur.execute(f'INSERT INTO {table} ({key_column}, {data_column})'
                    f'VALUES (%s, %s)', (key, data,))
        client.commit()
        client.close()

    @staticmethod
    def get_value(key, table, key_column, data_column, database, username,
                  password, host, port):
        client = psycopg2.connect(host=host, port=port, database=database,
                                  user=username, password=password)
        cur = client.cursor()
        cur.execute(f"SELECT {data_column} FROM {table} "
                    f"WHERE {key_column} like '{key}';")
        result = cur.fetchone()
        client.close()
        return result[0]


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


def set_value(obj, serializer, db_type, key, table=None, key_column=None,
              data_column=None, database=0, username=None, password=None,
              host='127.0.0.1', port='0'
              ):
    data = dumps(obj, serializer)
    CLASSES.get(db_type).set_value(data, key, table, key_column, data_column,
                                   database, username, password, host, port)


def get_value(key, serializer, db_type, table=None, key_column=None,
              data_column=None, database=0, username=None, password=None,
              host='127.0.0.1', port='0'
              ):
    data = CLASSES.get(db_type).get_value(key, table, key_column, data_column,
                                          database, username, password, host,
                                          port
                                          )
    return loads(data, serializer)
