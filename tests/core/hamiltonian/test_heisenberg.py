import numpy as np
from core.hamiltonian import HeisenbergHamiltonian, HamiltonianModel

class TestHeisenbergHamiltonian:
    def test_create_hamiltonian(self) -> None:
        n_qubits = 3
        coef = [0.5] * n_qubits
        got = HeisenbergHamiltonian(n_qubits, coef).create_hamiltonian()
        exp = [
            [ 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
            [ 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
            [ 0.+0.j, 1.+0.j,-1.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
            [ 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
            [ 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
            [ 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j,-1.+0.j, 1.+0.j, 0.+0.j],
            [ 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
            [ 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j],
        ]
        assert np.all(got == exp)

    def test_type(self) -> None:
        n_qubits = 3
        coef = [1.0] * n_qubits
        hamiltonian = HeisenbergHamiltonian(n_qubits, coef)
        assert hamiltonian.type == HamiltonianModel.HEISENBERG