from core.hamiltonian import IsingHamiltonian
from core.hamiltonian import HamiltonianModel

class TestIsingHamiltonian:
    def test_create_hamiltonian(self) -> None:
        n_qubits = 3
        coef = ([1.0] * n_qubits, [1.0] * n_qubits)
        hamiltonian = IsingHamiltonian(n_qubits, coef)
        ope = hamiltonian.create_hamiltonian()
        print(ope)
        assert False

    def test_type(self) -> None:
        n_qubits = 3
        coef = ([1.0] * n_qubits, [1.0] * n_qubits)
        hamiltonian = IsingHamiltonian(n_qubits, coef)
        assert(hamiltonian.type, HamiltonianModel.TRANSVERSE_ISING)