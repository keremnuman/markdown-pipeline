# doc2md

> Convert PDF, DOCX, and XLSX files to clean Markdown — one command, no API keys.

[![CI](https://github.com/keremnuman/markdown-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/keremnuman/markdown-pipeline/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Built for developers and teams who feed documents into LLMs or RAG pipelines.

---

## Installation

```bash
pip install doc2md
```

Or from source:

```bash
git clone https://github.com/keremnuman/markdown-pipeline.git
cd markdown-pipeline
pip install -e .
```

---

## CLI

```bash
# Single file
doc2md report.pdf

# Entire folder
doc2md ./documents --output ./output_md

# Parallel workers
doc2md ./documents --workers 8

# With config file
doc2md --config config.yaml
```

---

## Python API

```python
from pathlib import Path
from doc2md import MicrosoftMarkItDownConverter, DocumentPipeline

converter = MicrosoftMarkItDownConverter()
pipeline  = DocumentPipeline(converter=converter, output_dir=Path("./output"))

pipeline.process_single(Path("report.pdf"))   # single file
pipeline.process_batch(Path("./documents"))   # batch
```

---

## Contributing

```bash
git clone https://github.com/keremnuman/markdown-pipeline.git
pip install -e ".[dev]"
pytest tests/ -v
```

---

## License

MIT