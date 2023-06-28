from collections.abc import Sequence
from typing import Any

from google.cloud import bigquery


class BigQueryClient:
    def __init__(self, project_id: str):
        # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/serviceaccount.json'
        self.project_id = project_id
        self.client = bigquery.Client(project=project_id)

    def generate_table_id(self, project_id: str, dataset: str, table: str) -> bigquery.Table:
        return bigquery.Table.from_string(f"{project_id}.{dataset}.{table}")

    def create_table(
        self, dataset: str, table: str, schema: list[bigquery.SchemaField]
    ) -> bigquery.Table:
        table_id = bigquery.Table.from_string(f"{self.project_id}.{dataset}.{table}")
        table = bigquery.Table(table_id, schema=schema)  # type: ignore
        return self.client.create_table(table)

    def insert_rows(
        self, dataset: str, table: str, rows: Sequence[dict[str, Any]]
    ) -> Sequence[dict]:
        return self.client.insert_rows_json(
            self.generate_table_id(self.project_id, dataset, table), rows
        )
