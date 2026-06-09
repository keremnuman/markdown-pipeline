import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from doc2md import MicrosoftMarkItDownConverter, BaseDocumentConverter, ConversionError


def test_base_converter_is_abstract():
    with pytest.raises(TypeError):
        BaseDocumentConverter()


def test_markitdown_converter_returns_string(tmp_path):
    dummy_file = tmp_path / "test.pdf"
    dummy_file.write_text("dummy")

    mock_result = MagicMock()
    mock_result.text_content = "# Header\nContent"

    with patch("doc2md.converter.MarkItDown") as MockEngine:
        MockEngine.return_value.convert.return_value = mock_result
        converter = MicrosoftMarkItDownConverter()
        result = converter.convert(dummy_file)

    assert isinstance(result, str)
    assert result == "# Header\nContent"


def test_markitdown_converter_raises_conversion_error(tmp_path):
    dummy_file = tmp_path / "test.pdf"
    dummy_file.write_text("dummy")

    with patch("doc2md.converter.MarkItDown") as MockEngine:
        MockEngine.return_value.convert.side_effect = Exception("converter error")
        converter = MicrosoftMarkItDownConverter()

        with pytest.raises(ConversionError, match="converter error"):
            converter.convert(dummy_file)