
from dataclasses import dataclass

@dataclass
class Movie:
    title: str
    genre: str
    rating: float
    watched: bool
