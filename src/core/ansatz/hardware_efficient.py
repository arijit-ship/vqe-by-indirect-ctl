import numpy as np
from qulacs import QuantumCircuit
from qulacs.gate import CZ, RY, RZ, DepolarizingNoise, TwoQubitDepolarizingNoise, merge

from core.ansatz.ansatz import AnsatzType
from core.circuit import Noise

from . import AnsatzProtocol


class HardwareEfficientAnsatz(AnsatzProtocol):
    n_qubits: int
    depth: int
    noise: Noise
    _gate_set: int
    _parametric_circuit: QuantumCircuit

    def __init__(self, n_qubits: int, depth: int, noise: dict) -> None:
        self.n_qubits = n_qubits
        self.depth = depth
        single, two = 0, 0
        if noise["singlequbit"]["enabled"]:
            single = noise["singlequbit"]["value"]
        if noise["twoqubit"]["enabled"]:
            two = noise["twoqubit"]["value"]
        self.noise = Noise(single, two)

    @property
    def ansatz_type(self) -> AnsatzType:
        return AnsatzType.DIRECT

    @property
    def parametric_circuit(self) -> QuantumCircuit:
        return self._parametric_circuit

    def create_ansatz(self, params: list) -> QuantumCircuit:
        circuit = QuantumCircuit(self.n_qubits)
        for d in range(self.depth):
            for i in range(self.n_qubits):
                circuit = self.add_parametric_rotation_gate(
                    circuit,
                    i,
                    np.array(
                        [
                            params[2 * i + 2 * self.n_qubits * d],
                            params[2 * i + 1 + 2 * self.n_qubits * d],
                        ]
                    ),
                )
            for i in range(self.n_qubits // 2):
                circuit = self.add_cz_gate(circuit, 2 * i, 2 * i + 1)
                if (2 * i + 2) < self.n_qubits:
                    circuit = self.add_cz_gate(circuit, 2 * i + 1, 2 * i + 2)
        for i in range(self.n_qubits):
            circuit = self.add_parametric_rotation_gate(
                circuit,
                i,
                np.array(
                    [
                        params[2 * i + 2 * self.n_qubits * self.depth],
                        params[2 * i + 1 + 2 * self.n_qubits * self.depth],
                    ]
                ),
            )

        return circuit

    def add_parametric_rotation_gate(self, circuit, target_qubit, params):
        circuit.add_gate(
            merge(
                RY(target_qubit, params[0]),
                RZ(target_qubit, params[1]),
            )
        )
        if self.noise["singlequbit"]["enabled"]:
            circuit.add_gate(
                DepolarizingNoise(target_qubit, self.noise["singlequbit"]["value"])
            )
        return circuit

    def add_cz_gate(self, circuit, control_qubit, target_qubit):
        circuit.add_gate(CZ(control_qubit, target_qubit))

        if self.noise["twoqubit"]["enabled"]:
            circuit.add_gate(
                TwoQubitDepolarizingNoise(
                    control_qubit, target_qubit, self.noise["twoqubit"]["value"]
                )
            )
        return circuit
