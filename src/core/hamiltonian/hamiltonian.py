from abc import abstractproperty
from enum import Enum
from typing import Iterable, Protocol, Tuple, Union

import numpy as np
from typing_extensions import TypeAlias


class HamiltonianModel(Enum):
    TRANSVERSE_ISING = 1
    XY = 2
    HEISENBERG = 3


#: A type variable represents coefficients of each Hamiltonian term.
#: When you use Transverse Ising Hamiltonian(\sum a_j * X_j + \sum\sum J_jk * (Z_j Z_k) ), you can select Iterable[float, float].
#: First float is coefficient of X_j,  Second one is coefficient of Z_j Z_k.
Coefficients: TypeAlias = Union[
    Iterable[float], Tuple[Iterable[float], Iterable[float]]
]


class HamiltonianProtocol(Protocol):

    @abstractproperty
    def type(self) -> HamiltonianModel:
        ...

    @abstractproperty
    def value(self) -> np.ndarray:
        ...

    @abstractproperty
    def eigh(self) -> Tuple[np.ndarray, np.ndarray]:
        ...
