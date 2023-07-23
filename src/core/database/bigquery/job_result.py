import json
from collections.abc import Sequence
from typing import Any, Union

from google.cloud import bigquery

from ..schema.job import Job
from . import BigQueryClient
from .sql import sql_for_find_job


def create_job_result_table(client: BigQueryClient, dataset: str, table_name: str) -> None:
    schema = [
        bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("creation_time", "DATETIME"),
        bigquery.SchemaField("execution_second", "FLOAT64"),
        bigquery.SchemaField("n_qubits", "INTEGER"),
        bigquery.SchemaField("depth", "INTEGER"),
        bigquery.SchemaField("gate_type", "STRING"),
        bigquery.SchemaField("bn", "STRING"),
        bigquery.SchemaField("t", "STRING"),
        bigquery.SchemaField("cost", "STRING"),
        bigquery.SchemaField("parameter", "STRING"),
        bigquery.SchemaField("iteration", "STRING"),
        bigquery.SchemaField("cost_history", "STRING"),
        bigquery.SchemaField("parameter_history", "STRING"),
        bigquery.SchemaField("iteration_history", "STRING"),
        bigquery.SchemaField("config", "STRING"),
    ]
    table = client.create_table(dataset, table_name, schema)
    print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))


def insert_job_result(client: BigQueryClient, job: Job, dataset: str, table_name: str) -> None:
    row = vars(job)  # convert dict type
    row["creation_time"] = row["creation_time"].strftime(
        "%Y-%m-%d %H:%M:%S"
    )  # convert to str from datetime
    errors = client.insert_rows(dataset, table_name, [row])
    if errors == []:
        print("New rows have been added.")
    # else:
    #     print("Encountered errors while inserting rows: {}".format(errors))


def find_job_result(
    client: BigQueryClient,
    dataset: str,
    table_name: str,
    filter: Union[str, None] = None,
) -> Sequence[dict[str, Any]]:
    """Find job results of vqe expectation.

    Params are configured following values.

        client: A client to connect and operate BigQuery.
        filter: sql phrase to filter records. It excludes `filter`.
    """
    if filter is None:
        jobs = client.client.query(sql_for_find_job(client.project_id, dataset, table_name))
    else:
        jobs = client.client.query(
            "{} WHERE {}".format(sql_for_find_job(client.project_id, dataset, table_name), filter)
        )

    return _convert_queryjob_into_dict(jobs)


def _convert_queryjob_into_dict(jobs: Any) -> Sequence[dict[str, Any]]:
    rows = []
    for job in jobs:
        row = {}
        row["creation_time"] = job["creation_time"]
        row["execution_second"] = job["execution_second"]
        row["n_qubits"] = job["n_qubits"]
        row["depth"] = job["depth"]
        row["gate_type"] = job["gate_type"]
        row["gate_set"] = job["gate_set"]
        row["bn_type"] = job["bn_type"].strip("\"")
        row["bn_range"] = job["bn_range"]
        row["bn"] = job["bn"]
        row["cn"] = job["cn"]
        row["r"] = job["r"]
        row["t_type"] = job["t_type"].strip("\"")
        row["max_time"] = job["max_time"]
        row["min_time"] = job["min_time"]
        row["t"] = job["t"]
        row["cost"] = job["cost"]
        row["parameter"] = job["parameter"]
        row["iteration"] = job["iteration"]
        row["noise_singlequbit_enabled"] = job["noise_singlequbit_enabled"]
        row["noise_singlequbit_value"] = job["noise_singlequbit_value"].strip("\"")
        row["noise_twoqubit_enabled"] = job["noise_twoqubit_enabled"]
        row["noise_twoqubit_value"] = job["noise_twoqubit_value"].strip("\"")
        row["constraints"] = job["constraints"]
        row["bounds"] = job["bounds"]
        row["t_evol"] = job["t_evol"].strip("\"")
        row["config"] = json.loads(job["config"])
        rows.append(row)
    return rows
