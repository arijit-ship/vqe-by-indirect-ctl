from collections.abc import Sequence
from typing import Any
import json

from common.database.bigquery import BigQueryClient
from common.database.bigquery.sql.find_job import sql_for_find_job
from common.database.schema.job import Job
from google.cloud import bigquery

DATASET = "vqe"
TABLE = "job_result"


def create_job_result_table(client: BigQueryClient) -> None:
    schema = [
        bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("creation_time", "DATETIME"),
        bigquery.SchemaField("execution_second", "FLOAT64"),
        bigquery.SchemaField("nqubit", "INTEGER"),
        bigquery.SchemaField("depth", "INTEGER"),
        bigquery.SchemaField("gate_type", "STRING"),
        bigquery.SchemaField("gate_set", "STRING"),
        bigquery.SchemaField("bn_type", "STRING"),
        bigquery.SchemaField("bn_range", "INTEGER"),
        bigquery.SchemaField("bn", "STRING"),
        bigquery.SchemaField("cn", "STRING"),
        bigquery.SchemaField("r", "STRING"),
        bigquery.SchemaField("t_type", "STRING"),
        bigquery.SchemaField("min_time", "STRING"),
        bigquery.SchemaField("max_time", "STRING"),
        bigquery.SchemaField("t", "STRING"),
        bigquery.SchemaField("cost", "STRING"),
        bigquery.SchemaField("parameter", "STRING"),
        bigquery.SchemaField("iteration", "STRING"),
        bigquery.SchemaField("cost_history", "STRING"),
        bigquery.SchemaField("parameter_history", "STRING"),
        bigquery.SchemaField("iteration_history", "STRING"),
        bigquery.SchemaField("noise_singlequbit_enabled", "BOOL"),
        bigquery.SchemaField("noise_singlequbit_value", "STRING"),
        bigquery.SchemaField("noise_twoqubit_enabled", "BOOL"),
        bigquery.SchemaField("noise_twoqubit_value", "STRING"),
        bigquery.SchemaField("config", "STRING"),
    ]
    table = client.create_table(DATASET, TABLE, schema)
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )


def insert_job_result(client: BigQueryClient, job: Job) -> None:
    row = vars(job)  ## convert dict type
    row["creation_time"] = row["creation_time"].strftime(
        "%Y-%m-%d %H:%M:%S"
    )  ## convert to str from datetime
    errors = client.insert_rows(DATASET, TABLE, [row])
    if errors == []:
        print("New rows have been added.")
    # else:
    #     print("Encountered errors while inserting rows: {}".format(errors))


def find_job_result(
    client: BigQueryClient, filter: str = None
) -> Sequence[dict[str, Any]]:
    """
    Find job results of vqe expectation.

    Params are configured following values.

        client: A client to connect and operate BigQuery.
        filter: sql phrase to filter records. It excludes `filter`.
    """
    if filter is None:
        jobs = client.client.query(sql_for_find_job(client.project_id, DATASET))
    else:
        jobs = client.client.query(
            "{} WHERE {}".format(sql_for_find_job(client.project_id, DATASET), filter)
        )

    return _convert_queryjob_into_dict(jobs)


def _convert_queryjob_into_dict(jobs: Any) -> Sequence[dict[str, Any]]:
    rows = []
    for job in jobs:
        row = {}
        row["creation_time"] = job["creation_time"]
        row["execution_second"] = job["execution_second"]
        row["nqubit"] = job["nqubit"]
        row["depth"] = job["depth"]
        row["gate_type"] = job["gate_type"]
        row["gate_set"] = job["gate_set"]
        row["bn_type"] = job["bn_type"]
        row["bn_range"] = job["bn_range"]
        row["bn"] = job["bn"]
        row["cn"] = job["cn"]
        row["r"] = job["r"]
        row["t_type"] = job["t_type"]
        row["max_time"] = job["max_time"]
        row["min_time"] = job["min_time"]
        row["t"] = job["t"]
        row["cost"] = job["cost"]
        row["parameter"] = job["parameter"]
        row["iteration"] = job["iteration"]
        row["noise_singlequbit_enabled"] = job["noise_singlequbit_enabled"]
        row["noise_singlequbit_value"] = job["noise_singlequbit_value"]
        row["noise_twoqubit_enabled"] = job["noise_twoqubit_enabled"]
        row["noise_twoqubit_value"] = job["noise_twoqubit_value"]
        row["constraints"] = job["constraints"]
        row["bounds"] = job["bounds"]
        row["t_evol"] = job["t_evol"]
        row["config"] = json.loads(job["config"])
        rows.append(row)
    return rows
