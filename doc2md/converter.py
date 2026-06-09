from abc import ABC, abstractmethod
from pathlib import Path
from markitdown import MarkItDown


class ConversionError(Exception):
    pass


class BaseDocumentConverter(ABC):
    @abstractmethod
    def convert(self, source_path: Path) -> str:
        pass


class MicrosoftMarkItDownConverter(BaseDocumentConverter):
    def __init__(self):
        self._engine = MarkItDown()

    def convert(self, source_path: Path) -> str:
        try:
            result = self._engine.convert(str(source_path))
            return result.text_content
        except Exception as e:
            raise ConversionError(f"MarkItDown engine failed: {str(e)}")


def get_converter(name: str) -> BaseDocumentConverter:
    """Converter adına göre doğru sınıfı döndürür."""
    registry = {
        "markitdown": MicrosoftMarkItDownConverter,
    }
    if name not in registry:
        raise ValueError(
            f"Unknown converter '{name}'. Available: {list(registry.keys())}"
        )
    return registry[name]()