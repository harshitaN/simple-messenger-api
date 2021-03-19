from datetime import datetime, timedelta
import sqlite3


class InvalidParams(Exception):
    """
    Custom exception to raise error if invalid params
    """
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


def dict_factory(cursor, row):
    """
    dictionary factory for db connection rows
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connect_db():
    """
    Connects to sqlite DB and returns connection and cursor
    """
    conn = sqlite3.connect("messages.db")
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    return conn, cursor


def get_limit_query(limit, thirty_days, where_clause):
    """
    Gets part of the query based on limit param or thirty days param
    """
    if limit:
        return "LIMIT 100"
    elif thirty_days:
        # Since we are store epoch timestamp calculate the timestamp of 30 days ago
        thirty_days_ago = int((datetime.now() - timedelta(days=30)).timestamp())
        prefix = "WHERE " if where_clause else "AND "
        return prefix + "datetime > %d" % thirty_days_ago
    raise InvalidParams("Please specify message limit param or time limit param", status_code=400)