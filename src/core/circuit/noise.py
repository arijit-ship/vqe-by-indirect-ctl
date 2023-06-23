from dataclasses import dataclass
from typing import TypeAlias

NoiseValue: TypeAlias = float

@dataclass
class Noise():
    single: NoiseValue
    two: NoiseValue
 