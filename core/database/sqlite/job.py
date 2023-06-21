from pathlib import Path

from common.database.schema.job import Job
from common.database.sqlite import DBClient
from common.database.sqlite.sql.create_table_job import sql_for_create_table
from common.database.sqlite.sql.insert_job import sql_for_insert_job


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
            job.nqubit,
            job.depth,
            job.gate_type,
            job.gate_set,
            job.bn_type,
            job.bn_range,
            job.bn,
            job.cn,
            job.r,
            job.t_type,
            job.max_time,
            job.min_time,
            job.t,
            job.cost,
            job.parameter,
            job.iteration,
            job.cost_history,
            job.parameter_history,
            job.iteration_history,
            job.noise_singlequbit_enabled,
            job.noise_singlequbit_value,
            job.noise_twoqubit_enabled,
            job.noise_twoqubit_value,
            job.config,
        ),
    )
    client.conn.commit()
