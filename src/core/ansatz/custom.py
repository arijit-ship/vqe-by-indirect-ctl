from qulacs import ParametricQuantumCircuit

from core.ansatz.ansatz import AnsatzType
from core.circuit import Noise

from . import AnsatzProtocol


class HardwareEfficientAnsatz(AnsatzProtocol):
    n_qubits: int
    depth: int
    noise: Noise
    _gate_set: int
    _parametric_circuit: ParametricQuantumCircuit

    def __init__(
        self, n_qubits: int, depth: int, noise: dict, circuit: ParametricQuantumCircuit
    ) -> None:
        self.n_qubits = n_qubits
        self.depth = depth
        single, two = 0, 0
        if noise["singlequbit"]["enabled"]:
            single = noise["singlequbit"]["value"]
        if noise["twoqubit"]["enabled"]:
            two = noise["twoqubit"]["value"]
        self.noise = Noise(single, two)
        self._parametric_circuit = circuit

    @property
    def ansatz_type(self) -> AnsatzType:
        return AnsatzType.CUSTOM

    def create_ansatz(self, params: list) -> ParametricQuantumCircuit:
        for i, param in enumerate(params):
            self._parametric_circuit.set_parameter(i, param)
        return self._parametric_circuit
