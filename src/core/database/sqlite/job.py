from core.database.schema.job import Job

from .client import DBClient
from .sql.create_table_job import sql_for_create_table
from .sql.insert_job import sql_for_insert_job


def create_job_table(client: DBClient, force: bool = False) -> None:
    cur = client.conn.cursor()
    if force:
        cur.execute("DROP TABLE IF EXISTS jobs")

    cur.execute(sql_for_create_table())
    client.conn.commit()


def insert_job(client: DBClient, job: Job):
    cur = client.conn.cursor()
    cur.execute(
        sql_for_insert_job(),
        (
            job.id,
            job.creation_time,
            job.execution_second,
            job.n_qubits,
            job.depth,
            job.gate_type,
            job.bn,
            job.t,
            job.cost,
            job.parameter,
            job.iteration,
            job.cost_history,
            job.parameter_history,
            job.iteration_history,
            job.config,
        ),
    )
    client.conn.commit()
