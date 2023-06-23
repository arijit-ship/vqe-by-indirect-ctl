import sqlite3


class DBClient:
    def __init__(self, filepath):
        self.conn = sqlite3.connect(filepath)
