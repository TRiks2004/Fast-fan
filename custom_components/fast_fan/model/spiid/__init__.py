from dataclasses import dataclass


@dataclass(frozen=True)
class SPIID:
    siid: int
    piid: int