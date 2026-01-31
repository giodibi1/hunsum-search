from abc import ABC, abstractmethod
from typing import Any


class HunsumSearchInterface(ABC):
    @abstractmethod
    def search_body(self, query: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def search(self, query: str) -> list[dict[str, Any]]:
        pass
