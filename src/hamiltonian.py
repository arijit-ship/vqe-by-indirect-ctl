from openfermion.ops import QubitOperator
from qulacs.observable import create_observable_from_openfermion_text


def create_ising_hamiltonian(n_qubits):
    return create_observable_from_openfermion_text(
        str(_create_qubit_operator(n_qubits))
    )


def _create_qubit_operator(n_qubits):
    hami = QubitOperator()
    for i in range(n_qubits):
        hami = hami + QubitOperator("X" + str(i))
        for j in range(i + 1, n_qubits):
            if i + 1 == j:
                hami = hami + QubitOperator("Z" + str(i) + " " + "Z" + str(j))

    return hami
