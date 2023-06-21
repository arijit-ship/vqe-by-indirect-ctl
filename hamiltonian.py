from openfermion.ops import QubitOperator
from qulacs.observable import create_observable_from_openfermion_text


def create_ising_hamiltonian(nqubit):
    return create_observable_from_openfermion_text(str(create_qubit_operator(nqubit)))
    # transverse_Ising_hamiltonian = Observable(nqubit)
    # J = 1.0
    # h = 1.0
    # for i in range(nqubit):
    #     transverse_Ising_hamiltonian.add_operator(J, f"Z {i} Z {(i+1)%nqubit}")
    #     transverse_Ising_hamiltonian.add_operator(h, f"X {i}")
    # return transverse_Ising_hamiltonian


def create_qubit_operator(nqubit):
    hami = QubitOperator()
    for i in range(nqubit):
        hami = hami + QubitOperator("X" + str(i))
        for j in range(i + 1, nqubit):
            if i + 1 == j:
                hami = hami + QubitOperator("Z" + str(i) + " " + "Z" + str(j))

    return hami
