from dataclasses import dataclass

@dataclass
class State:
    id: str
    Name: str
    Capital: str
    Lat: int
    Lng: int
    Area: int
    Population: int
    Neighbors: str

    def __hash__(self):
        return hash(self.id)