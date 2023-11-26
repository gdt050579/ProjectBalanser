
from dataclasses import dataclass


@dataclass(frozen=True)
class Student:
    id: str
    name: str
    email: str

