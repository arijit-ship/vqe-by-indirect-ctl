import sqlite3
from job import insert_job, create_job_table


class DBClient:
    def __init__(self, filepath):
        self.conn = sqlite3.connect(filepath)
