from dataclasses import dataclass

from model.state import State


@dataclass
class Neighbors:
    stato1: State
    stato2: State