from collections.abc import Sequence
from typing import Any

from google.cloud import bigquery

from .job_result import create_job_result_table, find_job_result, insert_job_result

__all__ = [
    "create_job_result_table",
    "insert_job_result",
    "find_job_result",
]


class BigQueryClient:
    def __init__(self, project_id: str):
        # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/serviceaccount.json'
        self.project_id = project_id
        self.client = bigquery.Client(project=project_id)

    def generate_table_id(
        self, project_id: str, dataset: str, table: str
    ) -> bigquery.Table.table_id:
        return bigquery.Table.from_string(f"{project_id}.{dataset}.{table}")

    def create_table(self, dataset: str, table: str, schema: str) -> bigquery.Table:
        table_id = bigquery.Table.from_string(f"{self.project_id}.{dataset}.{table}")
        table = bigquery.Table(table_id, schema=schema)
        return self.client.create_table(table)

    def insert_rows(
        self, dataset: str, table: str, rows: Sequence[dict[str, Any]]
    ) -> Sequence[dict]:
        return self.client.insert_rows_json(
            self.generate_table_id(self.project_id, dataset, table), rows
        )
