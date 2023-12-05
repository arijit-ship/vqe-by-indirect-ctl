# sqlite3 schema

## jobs

| Column | Type | Description |
| ---- | ---- | ---- |
| id | char(36) PRIMARY KEY | unique id |
| creation_time | TIMESTAMP | execution datetime of vqe calculation |
| execution_second | INTEGER | execution time (sec) for vqe calculation |
| n_qubits | INTEGER | number of qubits |
| depth | INTEGER | number of layers in quantum circuit |
| gate_type | TEXT | type of indirect circuit. we have 3 types: "indirect_xy", "indirect_xyz", "indirect_ising" |
| bn | TEXT | magnetic field value as array |
| t | TEXT | time value as array |
| cost | TEXT | minimum enegy expectation value estimated by vqe |
| parameter | TEXT | parameters estimated by vqe |
| iteration | TEXT | number of iteration to optimize energy value |
| cost_history | TEXT | cost history of minimum enegy expectation value for each iteration |
| parameter_history | TEXT | parameter history of minimum enegy expectation value for each iteration |
| iteration_history | TEXT | history of iteration count |
| config | TEXT | configuration you used in a calculation. It can set in `config.yml` |
