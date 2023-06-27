import numpy as np

from core.hamiltonian import IsingHamiltonian, HamiltonianModel

class TestIsingHamiltonian:
    def test_create_hamiltonian(self) -> None:
        n_qubits = 3
        coef = ([1.0] * n_qubits, [1.0] * n_qubits)
        hamiltonian = IsingHamiltonian(n_qubits, coef)
        ope = hamiltonian.create_hamiltonian()
        expect = [
            [0.+0.j, 0.-1.j, 0.-1.j, 1.+0.j, 0.-1.j, 0.+0.j, 1.+0.j, 0.+0.j],
            [0.+1.j, 0.+0.j, 1.+0.j, 0.-1.j, 0.+0.j, 0.-1.j, 0.+0.j, 1.+0.j],
            [0.+1.j, 1.+0.j, 0.+0.j, 0.-1.j, 1.+0.j, 0.+0.j, 0.-1.j, 0.+0.j],
            [1.+0.j, 0.+1.j, 0.+1.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.-1.j],
            [0.+1.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.-1.j, 0.-1.j, 1.+0.j],
            [0.+0.j, 0.+1.j, 0.+0.j, 1.+0.j, 0.+1.j, 0.+0.j, 1.+0.j, 0.-1.j],
            [1.+0.j, 0.+0.j, 0.+1.j, 0.+0.j, 0.+1.j, 1.+0.j, 0.+0.j, 0.-1.j],
            [0.+0.j, 1.+0.j, 0.+0.j, 0.+1.j, 1.+0.j, 0.+1.j, 0.+1.j, 0.+0.j]
        ]
        assert(ope, expect)
        assert np.all(ope == expect)

    def test_type(self) -> None:
        n_qubits = 3
        coef = ([1.0] * n_qubits, [1.0] * n_qubits)
        hamiltonian = IsingHamiltonian(n_qubits, coef)
        assert(hamiltonian.type == HamiltonianModel.TRANSVERSE_ISING)