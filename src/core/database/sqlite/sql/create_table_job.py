def sql_for_create_table() -> str:
    return """
    CREATE TABLE jobs(
      id char(36) PRIMARY KEY,
      creation_time TIMESTAMP,
      execution_second INTEGER,
      n_qubits INTEGER,
      depth INTEGER,
      gate_type TEXT,
      bn TEXT,
      t TEXT,
      cost TEXT,
      parameter TEXT,
      iteration TEXT,
      cost_history TEXT,
      parameter_history TEXT,
      iteration_history TEXT,
      config TEXT
    )
    """
