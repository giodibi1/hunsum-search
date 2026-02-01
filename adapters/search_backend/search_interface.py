from abc import ABC, abstractmethod


class HunsumSearchInterface(ABC):
    class SearchFormatException(Exception):
        def __init__(self, message, error_code):
            super().__init__(message)
            self.error_code = error_code
            self.message = message

        def __str__(self):
            return f"{self.message} (Error Code: {self.error_code})"

    @abstractmethod
    def init_index(self, name: str, settings: dict):
        pass

    @abstractmethod
    def search_body(self, query: str):
        pass

    @abstractmethod
    def search(self, query: str):
        pass

    @abstractmethod
    def param_page(self, page_number: int = 1, page_size: int = 10):
        pass

    @abstractmethod
    def param_sort(self, sort_field: list[str]):
        pass

    @abstractmethod
    def param_filter(self, filter: list[str]):
        pass
