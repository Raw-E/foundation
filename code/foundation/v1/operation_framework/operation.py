# Standard library imports
from abc import ABC, abstractmethod
from typing import Any, Dict


class Operation(ABC):
    """
    Provides a framework for creating operations that can be executed asynchronously
    """

    def __init__(self, **kwargs: Any) -> None:
        self.__dict__.update(kwargs)

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Subclasses must implement execute method!")

    def __await__(self):
        """Allow the operation to be directly awaitable.

        Example:
        -------
        ```python
        class MyOperation(Operation):
            async def execute(self) -> str:
                return "Hello World"

        # Create and await the operation
        op = MyOperation()
        result = await op  # result will be "Hello World"

        # You can also pass parameters during initialization
        op_with_params = MyOperation(name="Alice", count=3)
        result = await op_with_params
        ```

        Returns:
        -------
        Awaitable
            Yields the result of the execute method.
        """
        return self.execute().__await__()

    def get_parameters(self) -> Dict[str, Any]:
        return self.__dict__.copy()
