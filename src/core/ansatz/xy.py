from qulacs import QuantumCircuit
from qulacs.gate import (
    CNOT,
    RY,
    RZ,
    DepolarizingNoise,
    TwoQubitDepolarizingNoise,
    merge,
)

from ..circuit import Noise, NoiseValue
from ..hamiltonian import XYHamiltonian

from . import AnsatzType, AnsatzWithTimeEvolutionGate


class XYAnsatz(AnsatzWithTimeEvolutionGate):
    n_qubits: int
    depth: int
    noise: Noise
    _gate_set: int
    _parametric_circuit: QuantumCircuit
    _hamiltonian: XYHamiltonian

    def __init__(
        self,
        n_qubits: int,
        depth: int,
        gate_set: int,
        noise: dict,
        hamiltonian: XYHamiltonian,
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
        return AnsatzType.INDIRECT_XY

    @property
    def parametric_circuit(self) -> QuantumCircuit:
        return self._parametric_circuit

    def create_ansatz(self, params: list) -> QuantumCircuit:
        """Create ansatz circuit When we create the time evolution gates, we
        need to give the time parameters.

        So we don't adopt ParametricQuantumCircuit, but QuantumCircuit.
        """
        circuit = QuantumCircuit(self.n_qubits)
        for d in range(self.depth):
            circuit.add_gate(CNOT(0, 1))
            if self.noise.two != 0:
                circuit.add_gate(TwoQubitDepolarizingNoise(0, 1, self.noise.two))

            circuit = self._add_parametric_rotation_gate(
                circuit,
                params[
                    self.depth
                    + 1
                    + (self._gate_set * d) : self.depth
                    + 1
                    + (self._gate_set * d)
                    + 4
                ],
            )

            circuit.add_gate(self.create_time_evolution_gate(params[d], params[d + 1]))

        return circuit

    def _add_parametric_rotation_gate(self, circuit, params) -> QuantumCircuit:
        circuit.add_gate(merge(RY(0, params[0]), RZ(0, params[1])))
        circuit.add_gate(merge(RY(1, params[2]), RZ(1, params[3])))

        if self.noise.single != 0:
            circuit.add_gate(DepolarizingNoise(0, self.noise.single))
            circuit.add_gate(DepolarizingNoise(1, self.noise.single))

        return circuit
