from qulacs import QuantumCircuit
from qulacs.gate import RX, RY, DepolarizingNoise, merge

from ..circuit import Noise
from ..hamiltonian import HeisenbergHamiltonian
from . import AnsatzType, AnsatzWithTimeEvolutionGate


class HeisenbergAnsatz(AnsatzWithTimeEvolutionGate):
    n_qubits: int
    depth: int
    noise: Noise
    _gate_set: int
    _hamiltonian: HeisenbergHamiltonian

    def __init__(
        self,
        n_qubits: int,
        depth: int,
        gate_set: int,
        noise: dict,
        hamiltonian: HeisenbergHamiltonian,
    ) -> None:
        self.n_qubits = n_qubits
        self.depth = depth
        self._gate_set = gate_set
        single, two = 0, 0
        if noise["singlequbit"]["enabled"]:
            single = noise["singlequbit"]["value"]
        if noise["twoqubit"]["enabled"]:
            two = noise["twoqubit"]["value"]
        self.noise = Noise(single, two)
        self._hamiltonian = hamiltonian

    @property
    def ansatz_type(self) -> AnsatzType:
        return AnsatzType.INDIRECT_HEISENBERG

    def create_ansatz(self, params: list) -> QuantumCircuit:
        """Create ansatz circuit When we create the time evolution gates, we
        need to give the time parameters.

        So we don't adopt ParametricQuantumCircuit, but QuantumCircuit.
        """
        circuit = QuantumCircuit(self.n_qubits)
        for d in range(self.depth):
            circuit.add_gate(
                merge(
                    RX(0, params[self.depth + 1 + (self._gate_set * d)]),
                    RY(0, params[self.depth + 1 + (self._gate_set * d) + 1]),
                )
            )
            if self.noise.single != 0:
                circuit.add_gate(DepolarizingNoise(0, self.noise.single))

            circuit.add_gate(self.create_time_evolution_gate(params[d], params[d + 1]))

        return circuit
