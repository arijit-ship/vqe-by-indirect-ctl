from functools import cached_property

import numpy as np

from ..circuit import PauliGate

from .hamiltonian import Coefficients, HamiltonianModel, HamiltonianProtocol


class XYHamiltonian(HamiltonianProtocol):
    def __init__(
        self,
        n_qubits: int,
        coef: Coefficients,
        gamma: float = 0,
    ) -> None:
        self.n_qubits = n_qubits
        self.coef = coef
        self.gamma = gamma

    @property
    def type(self) -> HamiltonianModel:
        return HamiltonianModel.XY

    @cached_property
    def value(self) -> np.ndarray:
        return self.create_hamiltonian()

    @cached_property
    def eigh(self) -> tuple[np.ndarray, np.ndarray]:
        return np.linalg.eigh(self.value)

    def create_hamiltonian(self) -> np.ndarray:
        XX = np.array(np.zeros(2**self.n_qubits))
        YY = np.array(np.zeros(2**self.n_qubits))
        Zn = np.array(np.zeros(2**self.n_qubits))
        for j in range(self.n_qubits - 1):
            for k in range(self.n_qubits):
                if j == k:
                    if k == 0:
                        hamiX = PauliGate.X_gate.value
                        hamiY = PauliGate.Y_gate.value
                    else:
                        hamiX = np.kron(hamiX, PauliGate.X_gate.value)
                        hamiY = np.kron(hamiY, PauliGate.Y_gate.value)

                elif j + 1 == k:
                    hamiX = np.kron(hamiX, PauliGate.X_gate.value)
                    hamiY = np.kron(hamiY, PauliGate.Y_gate.value)
                else:
                    if k == 0:
                        hamiX = PauliGate.I_gate.value
                        hamiY = PauliGate.I_gate.value
                    else:
                        hamiX = np.kron(hamiX, PauliGate.I_gate.value)
                        hamiY = np.kron(hamiY, PauliGate.I_gate.value)
            
            if not isinstance(self.coef, tuple):
                raise ValueError("coefficient must be tuple.")
            XX = XX + self.coef[0][j] * (1 + self.gamma) * hamiX
            YY = YY + self.coef[0][j] * (1 - self.gamma) * hamiY

        for m in range(self.n_qubits):
            for n in range(self.n_qubits):
                if m == n:
                    if n == 0:
                        hamiZ = PauliGate.Z_gate.value
                    else:
                        hamiZ = np.kron(hamiZ, PauliGate.Z_gate.value)

                else:
                    if n == 0:
                        hamiZ = PauliGate.I_gate.value
                    else:
                        hamiZ = np.kron(hamiZ, PauliGate.I_gate.value)

            if not isinstance(self.coef, tuple):
                raise ValueError("coefficient must be tuple.")
            Zn = Zn + self.coef[1][m] * hamiZ

        return XX + YY + Zn
