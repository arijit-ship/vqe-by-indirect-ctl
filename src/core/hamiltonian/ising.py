from functools import cached_property

import numpy as np

from ..circuit import PauliGate
from ..hamiltonian.hamiltonian import (
    Coefficients,
    HamiltonianModel,
    HamiltonianProtocol,
)


class IsingHamiltonian(HamiltonianProtocol):
    def __init__(self, n_qubits: int, coef: Coefficients) -> None:
        self.n_qubits = n_qubits
        self.coef = coef

    @property
    def type(self) -> HamiltonianModel:
        return HamiltonianModel.TRANSVERSE_ISING

    @cached_property
    def value(self) -> np.ndarray:
        return self.create_hamiltonian()

    @cached_property
    def eigh(self) -> tuple[np.ndarray, np.ndarray]:
        return np.linalg.eigh(self.value)

    def create_hamiltonian(self) -> np.ndarray:
        if not isinstance(self.coef, tuple):
            raise ValueError("coef must be tuple")
        XX = np.array(np.zeros(2**self.n_qubits))
        Y = np.array(np.zeros(2**self.n_qubits))
        for j in range(self.n_qubits - 1):
            for k in range(self.n_qubits):
                if j == k:
                    if k == 0:
                        hamiX = np.array(PauliGate.X_gate.value)
                    else:
                        hamiX = np.kron(hamiX, PauliGate.X_gate.value)

                elif j + 1 == k:
                    hamiX = np.kron(hamiX, PauliGate.X_gate.value)
                else:
                    if k == 0:
                        hamiX = np.array(PauliGate.I_gate.value)
                    else:
                        hamiX = np.kron(hamiX, PauliGate.I_gate.value)
            XX = XX + self.coef[0][j] * hamiX

        for m in range(self.n_qubits):
            for n in range(self.n_qubits):
                if m == n:
                    if n == 0:
                        hamiY = np.array(PauliGate.Y_gate.value)
                    else:
                        hamiY = np.kron(hamiY, PauliGate.Y_gate.value)

                else:
                    if n == 0:
                        hamiY = np.array(PauliGate.I_gate.value)
                    else:
                        hamiY = np.kron(hamiY, PauliGate.I_gate.value)

            Y = Y + self.coef[1][m] * hamiY

        return XX + Y
