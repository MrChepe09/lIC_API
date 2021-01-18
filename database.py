from flask import g
import sqlite3
import os
basedir = os.path.abspath(os.path.dirname(__file__))

def connect_db():
    sql = sqlite3.connect(os.path.join(basedir, 'members.db'))
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db