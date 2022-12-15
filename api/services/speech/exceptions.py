import dataclasses
@dataclasses.dataclass
class MinDurationException(Exception):
    got: int
    want: int

@dataclasses.dataclass
class MaxDurationException(Exception):
    got: int
    want: int

