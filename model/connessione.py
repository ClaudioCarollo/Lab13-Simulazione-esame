from dataclasses import dataclass

from model.state import State


@dataclass
class Neighbor:
    stato1: State
    stato2: State
