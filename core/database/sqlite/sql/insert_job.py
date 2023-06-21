def sql_for_insert_job() -> str:
    return """
    INSERT INTO jobs (
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
        cost_history,
        parameter_history,
        iteration_history,
        noise_singlequbit_enabled,
        noise_singlequbit_value,
        noise_twoqubit_enabled,
        noise_twoqubit_value,
        config
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """
