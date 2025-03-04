from abc import ABC, abstractmethod
from typing import Any, Dict


class Operation(ABC):
    def __init__(self, **kwargs: Any) -> None:
        self.__dict__.update(kwargs)

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Subclasses must implement execute method!")

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.execute(*args, **kwargs)

    def __await__(self):
        return self.execute().__await__()

    def get_parameters(self) -> Dict[str, Any]:
        return self.__dict__.copy()
