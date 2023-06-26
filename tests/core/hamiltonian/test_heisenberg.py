from core.hamiltonian import HeisenbergHamiltonian

class TestHeisenbergHamiltonian:
    def test_create_hamiltonian(self) -> None:
        n_qubits = 3
        coef = [1.0] * n_qubits
        hamiltonian = HeisenbergHamiltonian(n_qubits, coef)
        ope = hamiltonian.create_hamiltonian()
        print(ope)
        assert False
