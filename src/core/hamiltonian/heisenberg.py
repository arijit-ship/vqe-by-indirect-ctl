from functools import cached_property

import numpy as np

from ..circuit import PauliGate
from .hamiltonian import Coefficients, HamiltonianModel, HamiltonianProtocol


class HeisenbergHamiltonian(HamiltonianProtocol):
    def __init__(
        self,
        n_qubits: int,
        coef: Coefficients,
    ) -> None:
        self.n_qubits = n_qubits
        self.coef = coef

    @property
    def type(self) -> HamiltonianModel:
        return HamiltonianModel.HEISENBERG

    @cached_property
    def value(self) -> np.ndarray:
        return self.create_hamiltonian()

    @cached_property
    def eigh(self) -> tuple[np.ndarray, np.ndarray]:
        return np.linalg.eigh(self.value)

    def create_hamiltonian(self) -> np.ndarray:
        XX = np.array(np.zeros(2**self.n_qubits))
        YY = np.array(np.zeros(2**self.n_qubits))
        ZZ = np.array(np.zeros(2**self.n_qubits))
        for k in range(self.n_qubits - 1):
            for l in range(self.n_qubits):
                if k == l:
                    if l == 0:
                        hamiX = PauliGate.X_gate.value
                        hamiY = PauliGate.Y_gate.value
                        hamiZ = PauliGate.Z_gate.value
                    else:
                        hamiX = np.kron(hamiX, PauliGate.X_gate.value)
                        hamiY = np.kron(hamiY, PauliGate.Y_gate.value)
                        hamiZ = np.kron(hamiZ, PauliGate.Z_gate.value)

                elif k + 1 == l:
                    hamiX = np.kron(hamiX, PauliGate.X_gate.value)
                    hamiY = np.kron(hamiY, PauliGate.Y_gate.value)
                    hamiZ = np.kron(hamiZ, PauliGate.Z_gate.value)
                else:
                    if l == 0:
                        hamiX = PauliGate.I_gate.value
                        hamiY = PauliGate.I_gate.value
                        hamiZ = PauliGate.I_gate.value
                    else:
                        hamiX = np.kron(hamiX, PauliGate.I_gate.value)
                        hamiY = np.kron(hamiY, PauliGate.I_gate.value)
                        hamiZ = np.kron(hamiZ, PauliGate.I_gate.value)
            if not isinstance(self.coef, list):
                raise ValueError("coefficient must be list[float].")
            XX = XX + self.coef[k] * hamiX
            YY = YY + self.coef[k] * hamiY
            ZZ = ZZ + self.coef[k] * hamiZ

        return XX + YY + ZZ
