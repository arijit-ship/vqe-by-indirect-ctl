import argparse
import datetime
import time

import yaml
from qulacs import QuantumCircuit, QuantumState
from scipy.optimize import minimize

from core.ansatz import AnsatzProtocol, HeisenbergAnsatz, IsingAnsatz, XYAnsatz
from core.database.bigquery import (
    BigQueryClient,
    create_job_result_table,
    insert_job_result,
)
from core.database.schema import Job, JobFactory
from core.database.sqlite import DBClient, create_job_table, insert_job
from core.hamiltonian import HeisenbergHamiltonian, IsingHamiltonian, XYHamiltonian
from observable import create_ising_hamiltonian
from params import create_init_params
from constraints import create_time_constraints

iteration = 0
param_history = []
cost_history = []
iter_history = []


def reset():
    global param_history
    global cost_history
    global iter_history
    global iteration
    param_history = []
    cost_history = []
    iter_history = []
    iteration = 0


def init_ansatz(
    n_qubits: int,
    depth: int,
    gate_type: str,
    gate_set: int,
    noise: dict,
    bn_coef: list,
) -> AnsatzProtocol:
    ansatz: AnsatzProtocol
    if gate_type == "direct":
        ...
        # ansatz = HardwareEfficientAnsatz(n_qubits, depth, noise)
    elif gate_type == "indirect_xy":
        xy_coef = ([0.5] * n_qubits, bn_coef)
        xy_hami = XYHamiltonian(n_qubits, xy_coef, gamma=0)
        ansatz = XYAnsatz(n_qubits, depth, gate_set, noise, xy_hami)
    elif gate_type == "indirect_ising":
        ising_coef = ([0.5] * n_qubits, [1.0] * n_qubits)
        ising_hami = IsingHamiltonian(n_qubits, ising_coef)
        ansatz = IsingAnsatz(n_qubits, depth, gate_set, noise, ising_hami)
    elif gate_type == "indirect_heisenberg":
        heisenberg_coef = [1.0] * n_qubits
        heisenberg_hami = HeisenbergHamiltonian(n_qubits, heisenberg_coef)
        ansatz = HeisenbergAnsatz(n_qubits, depth, gate_set, noise, heisenberg_hami)
    return ansatz


def cost(n_qubits, ansatz, observable, params):
    global iteration
    iteration += 1
    state = QuantumState(n_qubits)
    circuit = QuantumCircuit(n_qubits)
    circuit = ansatz.create_ansatz(params)
    circuit.update_quantum_state(state)
    return observable.get_expectation_value(state)


def record(n_qubits, ansatz, observable, params):
    global param_history
    global cost_history
    global iter_history
    global iteration
    param_history.append(params)
    cost_history.append(cost(n_qubits, ansatz, observable, params))
    iter_history.append(iteration)


def record_database(
    job: Job, is_bq_import: bool, gcp_project_id: str, dataset: str, table: str
) -> None:
    client = DBClient("data/job_results.sqlite3")
    insert_job(client, job)
    if is_bq_import:
        bq_client = BigQueryClient(gcp_project_id)
        insert_job_result(bq_client, job, dataset, table)


def run(config):
    # performance measurement
    start_time = time.perf_counter()
    now = datetime.datetime.now()

    n_qubits = config["n_qubits"]
    # init qulacs hamiltonian
    observable = create_ising_hamiltonian(n_qubits)

    # init ansatz instance
    ansatz = init_ansatz(
        n_qubits,
        config["depth"],
        config["gate"]["type"],
        config["gate"]["parametric_rotation_gate_set"],
        config["gate"]["noise"],
        config["gate"]["bn"]["value"],
    )

    # randomize and create constraints
    init_params, _ = create_init_params(config)
    constraints = create_time_constraints(config["depth"] + 1, len(init_params))
    record(n_qubits, ansatz, observable, init_params)

    def record_fn(params):
        return record(n_qubits, ansatz, observable, params)

    def cost_fn(params):
        return cost(n_qubits, ansatz, observable, params)

    # calculation
    options = {"maxiter": 2000}
    _ = minimize(
        cost_fn,
        init_params,
        method=config["optimizer"]["method"],
        constraints=constraints,
        options=options,
        callback=record_fn,
    )

    end_time = time.perf_counter()

    print(cost_history)
    # record to database
    job = JobFactory(config).create(
        now, start_time, end_time, cost_history, param_history, iter_history
    )
    record_database(
        job,
        config["gcp"]["bigquery"]["import"],
        config["gcp"]["project"]["id"],
        config["gcp"]["bigquery"]["dataset"],
        config["gcp"]["bigquery"]["table"],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--init", type=bool, required=False)
    args = parser.parse_args()
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)
        if args.init:
            client = DBClient("data/job_results.sqlite3")
            create_job_table(client)
            if config["gcp"]["bigquery"]["import"]:
                bq_client = BigQueryClient(
                    config["gcp"]["project"]["id"],
                )
                create_job_result_table(
                    bq_client,
                    config["gcp"]["bigquery"]["dataset"],
                    config["gcp"]["bigquery"]["table"],
                )
        else:
            for k in range(config["iter"]):
                run(config)
                reset()
