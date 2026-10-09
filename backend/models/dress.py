from dataclasses import dataclass
from linked_list import LinkedList

@dataclass
class Dress:
    _next_id: ClassVar[int] = 1

    designer: str
    color: str
    size: str
    price: float
    image_path: str

    dress_id: int = field(init=False)
    dress_history: LinkedList = field(default_factory=LinkedList)

    def __post_init__(self):
        self.dress_id = Dress._next_id
        Dress._next_id += 1