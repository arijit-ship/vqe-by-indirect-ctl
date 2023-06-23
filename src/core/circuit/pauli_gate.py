from enum import Enum


class PauliGate(Enum):
    I_gate = [[1, 0], [0, 1]]
    X_gate = [[0, 1], [1, 0]]
    Y_gate = [[0, 0 - 1j], [0 + 1j, 0]]
    Z_gate = [[1, 0], [0, -1]]
