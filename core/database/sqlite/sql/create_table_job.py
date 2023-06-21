def sql_for_create_table() -> str:
    return """
    CREATE TABLE jobs(
      id char(36) PRIMARY KEY,
      creation_time TIMESTAMP,
      execution_second INTEGER,
      nqubit INTEGER,
      depth INTEGER,
      gate_type TEXT,
      gate_set TEXT,
      bn_type TEXT,
      bn_range INTEGER,
      bn TEXT,
      cn TEXT,
      r TEXT,
      t_type TEXT,
      min_time TEXT,
      max_time TEXT,
      t TEXT,
      cost TEXT,
      parameter TEXT,
      iteration TEXT,
      cost_history TEXT,
      parameter_history TEXT,
      iteration_history TEXT,
      noise_singlequbit_enabled TEXT,
      noise_singlequbit_value TEXT,
      noise_twoqubit_enabled TEXT,
      noise_twoqubit_value TEXT,
      config TEXT
    )
    """
