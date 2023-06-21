def sql_for_find_job(project_id: str, dataset: str) -> str:
    return f"""
        SELECT
            id,
            creation_time,
            execution_second,
            nqubit,
            depth,
            gate_type,
            gate_set,
            bn_type,
            bn_range,
            bn,
            cn,
            r,
            t_type,
            max_time,
            min_time,
            t,
            cost,
            parameter,
            iteration,
            noise_singlequbit_enabled,
            noise_singlequbit_value,
            noise_twoqubit_enabled,
            noise_twoqubit_value,
            json_extract(config, "$.gate.constraints") as constraints,
            json_extract(config, "$.gate.bounds") as bounds,
            json_extract(config, "$.gate.time.evol") as t_evol,
            config
        FROM {project_id}.{dataset}.job_result
    """
