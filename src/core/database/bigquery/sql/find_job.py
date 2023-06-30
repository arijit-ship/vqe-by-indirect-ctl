def sql_for_find_job(project_id: str, dataset: str, table_name: str) -> str:
    return f"""
        SELECT
            id,
            creation_time,
            execution_second,
            n_qubits,
            depth,
            gate_type,
            json_extract(config, "$.gate.parametric_rotation_gate_set") as gate_set,
            json_extract(config, "$.gate.bn.type") as bn_type,
            json_extract(config, "$.gate.bn.range") as bn_range,
            bn,
            json_extract(config, "$.gate.cn.value") as cn,
            json_extract(config, "$.gate.r.value") as r,
            json_extract(config, "$.gate.time.type") as t_type,
            json_extract(config, "$.gate.time.max_val") as max_time,
            json_extract(config, "$.gate.time.min_val") as min_time,
            t,
            cost,
            parameter,
            iteration,
            json_extract(config, "$.gate.noise.singlequbit.enabled") as noise_singlequbit_enabled,
            json_extract(config, "$.gate.noise.singlequbit.value") as noise_singlequbit_value,
            json_extract(config, "$.gate.noise.twoqubit.enabled") as noise_twoqubit_enabled,
            json_extract(config, "$.gate.noise.twoqubit.value") as noise_twoqubit_value,
            json_extract(config, "$.gate.constraints") as constraints,
            json_extract(config, "$.gate.bounds") as bounds,
            json_extract(config, "$.gate.time.evol") as t_evol,
            config
        FROM {project_id}.{dataset}.{table_name}
    """
