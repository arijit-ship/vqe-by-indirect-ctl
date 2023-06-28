import numpy as np

from core.hamiltonian import HamiltonianModel, IsingHamiltonian


class TestIsingHamiltonian:
    def test_create_hamiltonian(self) -> None:
        n_qubits = 3
        coef = ([1.0] * n_qubits, [1.0] * n_qubits)
        got = IsingHamiltonian(n_qubits, coef).create_hamiltonian()
        exp = [
            [
                0.0 + 0.0j,
                0.0 - 1.0j,
                0.0 - 1.0j,
                1.0 + 0.0j,
                0.0 - 1.0j,
                0.0 + 0.0j,
                1.0 + 0.0j,
                0.0 + 0.0j,
            ],
            [
                0.0 + 1.0j,
                0.0 + 0.0j,
                1.0 + 0.0j,
                0.0 - 1.0j,
                0.0 + 0.0j,
                0.0 - 1.0j,
                0.0 + 0.0j,
                1.0 + 0.0j,
            ],
            [
                0.0 + 1.0j,
                1.0 + 0.0j,
                0.0 + 0.0j,
                0.0 - 1.0j,
                1.0 + 0.0j,
                0.0 + 0.0j,
                0.0 - 1.0j,
                0.0 + 0.0j,
            ],
            [
                1.0 + 0.0j,
                0.0 + 1.0j,
                0.0 + 1.0j,
                0.0 + 0.0j,
                0.0 + 0.0j,
                1.0 + 0.0j,
                0.0 + 0.0j,
                0.0 - 1.0j,
            ],
            [
                0.0 + 1.0j,
                0.0 + 0.0j,
                1.0 + 0.0j,
                0.0 + 0.0j,
                0.0 + 0.0j,
                0.0 - 1.0j,
                0.0 - 1.0j,
                1.0 + 0.0j,
            ],
            [
                0.0 + 0.0j,
                0.0 + 1.0j,
                0.0 + 0.0j,
                1.0 + 0.0j,
                0.0 + 1.0j,
                0.0 + 0.0j,
                1.0 + 0.0j,
                0.0 - 1.0j,
            ],
            [
                1.0 + 0.0j,
                0.0 + 0.0j,
                0.0 + 1.0j,
                0.0 + 0.0j,
                0.0 + 1.0j,
                1.0 + 0.0j,
                0.0 + 0.0j,
                0.0 - 1.0j,
            ],
            [
                0.0 + 0.0j,
                1.0 + 0.0j,
                0.0 + 0.0j,
                0.0 + 1.0j,
                1.0 + 0.0j,
                0.0 + 1.0j,
                0.0 + 1.0j,
                0.0 + 0.0j,
            ],
        ]
        assert np.all(got == exp)

        coef = ([0.5] * n_qubits, [1.0] * n_qubits)
        got = IsingHamiltonian(n_qubits, coef).create_hamiltonian()
        exp = [
            [
                0.0 + 0.0j,
                0.0 - 1.0j,
                0.0 - 1.0j,
                0.5 + 0.0j,
                0.0 - 1.0j,
                0.0 + 0.0j,
                0.5 + 0.0j,
                0.0 + 0.0j,
            ],
            [
                0.0 + 1.0j,
                0.0 + 0.0j,
                0.5 + 0.0j,
                0.0 - 1.0j,
                0.0 + 0.0j,
                0.0 - 1.0j,
                0.0 + 0.0j,
                0.5 + 0.0j,
            ],
            [
                0.0 + 1.0j,
                0.5 + 0.0j,
                0.0 + 0.0j,
                0.0 - 1.0j,
                0.5 + 0.0j,
                0.0 + 0.0j,
                0.0 - 1.0j,
                0.0 + 0.0j,
            ],
            [
                0.5 + 0.0j,
                0.0 + 1.0j,
                0.0 + 1.0j,
                0.0 + 0.0j,
                0.0 + 0.0j,
                0.5 + 0.0j,
                0.0 + 0.0j,
                0.0 - 1.0j,
            ],
            [
                0.0 + 1.0j,
                0.0 + 0.0j,
                0.5 + 0.0j,
                0.0 + 0.0j,
                0.0 + 0.0j,
                0.0 - 1.0j,
                0.0 - 1.0j,
                0.5 + 0.0j,
            ],
            [
                0.0 + 0.0j,
                0.0 + 1.0j,
                0.0 + 0.0j,
                0.5 + 0.0j,
                0.0 + 1.0j,
                0.0 + 0.0j,
                0.5 + 0.0j,
                0.0 - 1.0j,
            ],
            [
                0.5 + 0.0j,
                0.0 + 0.0j,
                0.0 + 1.0j,
                0.0 + 0.0j,
                0.0 + 1.0j,
                0.5 + 0.0j,
                0.0 + 0.0j,
                0.0 - 1.0j,
            ],
            [
                0.0 + 0.0j,
                0.5 + 0.0j,
                0.0 + 0.0j,
                0.0 + 1.0j,
                0.5 + 0.0j,
                0.0 + 1.0j,
                0.0 + 1.0j,
                0.0 + 0.0j,
            ],
        ]
        assert np.all(got == exp)

    def test_type(self) -> None:
        n_qubits = 3
        coef = ([1.0] * n_qubits, [1.0] * n_qubits)
        hamiltonian = IsingHamiltonian(n_qubits, coef)
        assert hamiltonian.type == HamiltonianModel.TRANSVERSE_ISING
