from qulacs import QuantumCircuit
from qulacs.gate import RY, RZ, DepolarizingNoise, merge

from ..circuit import Noise
from ..hamiltonian import HeisenbergHamiltonian
from . import AnsatzType, AnsatzWithTimeEvolutionGate


class HeisenbergAnsatz(AnsatzWithTimeEvolutionGate):
    n_qubits: int
    depth: int
    noise: Noise
    _gate_set: int
    _parametric_circuit: QuantumCircuit
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

    @property
    def parametric_circuit(self) -> QuantumCircuit:
        return self._parametric_circuit

    def create_ansatz(self, params: list) -> QuantumCircuit:
        """Create ansatz circuit When we create the time evolution gates, we
        need to give the time parameters.

        So we don't adopt ParametricQuantumCircuit, but QuantumCircuit.
        """
        circuit = QuantumCircuit(self.nqubit)
        for d in range(self.depth):
            if self.bn["type"] == "random":
                circuit.add_gate(
                    RZ(
                        0,
                        params[
                            self.depth
                            + (self.depth * self.nqubit)
                            + (self.gate_set * d)
                        ],
                    )
                )
                circuit.add_gate(
                    RZ(
                        1,
                        params[
                            self.depth
                            + (self.depth * self.nqubit)
                            + (self.gate_set * d)
                            + 1
                        ],
                    )
                )
                circuit.add_gate(
                    self.create_hamiltonian_gate(
                        params[d + self.depth : d + self.depth + self.nqubit],
                        params[d],
                    )
                )
            elif self.bn["type"] == "static" or self.bn["type"] == "static_random":
                if self.time["type"] == "random":
                    circuit.add_gate(RZ(0, params[self.depth + (self._gate_set * d)]))
                    circuit.add_gate(
                        RZ(1, params[self.depth + (self._gate_set * d) + 1])
                    )
                    circuit.add_gate(self.create_hamiltonian_gate(params[d]))
                else:
                    circuit.add_gate(RZ(0, params[(self._gate_set * d)]))
                    circuit.add_gate(RZ(1, params[(self._gate_set * d) + 1]))
                    circuit.add_gate(self.create_hamiltonian_gate(self.time["min_val"]))

        return circuit

    def _add_parametric_rotation_gate(self, circuit, params) -> QuantumCircuit:
        circuit.add_gate(merge(RY(0, params[0]), RZ(0, params[1])))
        circuit.add_gate(merge(RY(1, params[2]), RZ(1, params[3])))

        if self.noise.single != 0:
            circuit.add_gate(DepolarizingNoise(0, self.noise.single))
            circuit.add_gate(DepolarizingNoise(1, self.noise.single))

        return circuit
