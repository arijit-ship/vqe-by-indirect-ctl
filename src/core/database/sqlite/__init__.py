import sqlite3

from job import create_job_table, insert_job

__all__ = [
    "insert_job",
    "create_job_table",
]


class DBClient:
    def __init__(self, filepath):
        self.conn = sqlite3.connect(filepath)
