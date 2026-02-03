from abc import ABC, abstractmethod
from typing import Any
import adapters.search_backend.search_impl as search_impl
import schemas.document_schema as document_schema


class HunsumSearchInterface(ABC):
    class SearchFormatException(Exception):
        def __init__(self, message, error_code):
            super().__init__(message)
            self.error_code = error_code
            self.message = message

        def __str__(self):
            return f"{self.message} (Error Code: {self.error_code})"

    @abstractmethod
    def init_index(self, name: str, settings: dict) -> bool:
        pass

    @abstractmethod
    def del_index(self, name: str) -> bool:
        pass

    @abstractmethod
    def upload_doc(self, index_name: str, doc: document_schema.Document) -> bool:
        pass

    @abstractmethod
    def search_body(self, query: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def search(self, query: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def param_page(self, page_number: int = 1, page_size: int = 10) -> dict[str, int]:
        pass

    @abstractmethod
    def param_sort(self, sort_field: list[str]) -> list[any]:
        pass

    @abstractmethod
    def param_filter(self, filter: list[str]) -> list[dict[str, dict]]:
        pass
