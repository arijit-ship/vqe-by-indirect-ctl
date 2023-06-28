from qulacs import QuantumCircuit
from core.ansatz.ansatz import AnsatzType
from . import AnsatzProtocol
from core.circuit import Noise

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
    
    def ansatz_type(self) -> AnsatzType:
        return AnsatzType.DIRECT
    
    def parametric_circuit(self) -> QuantumCircuit:
        return self._parametric_circuit
    
    def create_ansatz(self, params: list) -> QuantumCircuit:
        ...