from typing import TypeAlias
from dataclasses import dataclass

NoiseValue: TypeAlias = float

@dataclass
class Noise():
    single: NoiseValue
    two: NoiseValue
 