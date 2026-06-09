import pytest
from pathlib import Path
from unittest.mock import MagicMock
from doc2md import DocumentPipeline, ConversionError


@pytest.fixture
def mock_converter():
    converter = MagicMock()
    converter.convert.return_value = "# Test Content"
    return converter


@pytest.fixture
def pipeline(mock_converter, tmp_path):
    return DocumentPipeline(converter=mock_converter, output_dir=tmp_path / "output")


def test_output_dir_created(mock_converter, tmp_path):
    out = tmp_path / "new folder"
    assert not out.exists()
    DocumentPipeline(converter=mock_converter, output_dir=out)
    assert out.exists()


def test_process_single_success(pipeline, tmp_path):
    pdf = tmp_path / "report.pdf"
    pdf.write_text("dummy")

    result = pipeline.process_single(pdf)

    assert result is not None
    assert result.suffix == ".md"
    assert result.read_text(encoding="utf-8") == "# Test Content"


def test_process_single_unsupported_format(pipeline, tmp_path):
    txt = tmp_path / "file.txt"
    txt.write_text("Content")

    result = pipeline.process_single(txt)
    assert result is None


def test_process_single_missing_file(pipeline, tmp_path):
    result = pipeline.process_single(tmp_path / "bogus.pdf")
    assert result is None


def test_process_single_conversion_error(pipeline, mock_converter, tmp_path):
    mock_converter.convert.side_effect = ConversionError("hata")
    pdf = tmp_path / "broken.pdf"
    pdf.write_text("dummy")

    result = pipeline.process_single(pdf)
    assert result is None


def test_process_batch_returns_successful_paths(pipeline, tmp_path):
    (tmp_path / "a.pdf").write_text("dummy")
    (tmp_path / "b.docx").write_text("dummy")
    (tmp_path / "c.txt").write_text("dummy")   # desteklenmiyor

    results = pipeline.process_batch(tmp_path)

    assert len(results) == 2
    assert all(r.suffix == ".md" for r in results)


def test_process_batch_partial_failure(pipeline, mock_converter, tmp_path):
    good = tmp_path / "good.pdf"
    bad  = tmp_path / "bad.pdf"
    good.write_text("dummy")
    bad.write_text("dummy")

    def side_effect(path):
        if path.name == "bad.pdf":
            raise ConversionError("error")
        return "# Content"

    mock_converter.convert.side_effect = side_effect
    results = pipeline.process_batch(tmp_path)

    assert len(results) == 1
    assert results[0].stem == "good"

def test_process_batch_parallel(pipeline, tmp_path):
    for i in range(4):
        (tmp_path / f"doc{i}.pdf").write_text("dummy")

    pipeline.max_workers = 2
    results = pipeline.process_batch(tmp_path)
    assert len(results) == 4   