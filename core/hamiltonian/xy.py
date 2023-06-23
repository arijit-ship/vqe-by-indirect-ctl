from functools import cached_property
from typing import Tuple
import numpy as np
from core.circuit import PauliGate
from .hamiltonian import HamiltonianModel, HamiltonianProtocol, Coefficients


class XYHamiltonian(HamiltonianProtocol):
    def __init__(
        self, n_qubits: int, coef: Coefficients, gamma: float = 0,
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
    def eigh(self) -> Tuple:
        return np.linalg.eigh(self.value)
    
    def create_hamiltonian(self) -> np.ndarray:
        XX = np.array(np.zeros(2**self.n_qubits))
        YY = np.array(np.zeros(2**self.n_qubits))
        Zn = np.array(np.zeros(2**self.n_qubits))
        for k in range(self.n_qubits - 1):
            for l in range(self.n_qubits):
                if k == l:
                    if l == 0:
                        hamiX = PauliGate.X_gate.value
                        hamiY = PauliGate.Y_gate.value
                    else:
                        hamiX = np.kron(hamiX, PauliGate.X_gate.value)
                        hamiY = np.kron(hamiY, PauliGate.Y_gate.value)

                elif k + 1 == l:
                    hamiX = np.kron(hamiX, PauliGate.X_gate.value)
                    hamiY = np.kron(hamiY, PauliGate.Y_gate.value)
                else:
                    if l == 0:
                        hamiX = PauliGate.I_gate.value
                        hamiY = PauliGate.I_gate.value
                    else:
                        hamiX = np.kron(hamiX, PauliGate.I_gate.value)
                        hamiY = np.kron(hamiY, PauliGate.I_gate.value)
            XX = XX + self.coef[0][k] * (1 + self.gamma) * hamiX
            YY = YY + self.coef[0][k] * (1 - self.gamma) * hamiY

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

            Zn = Zn + self.coef[1][m] * hamiZ

        return XX + YY + Zn