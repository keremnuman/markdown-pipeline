# PDF to Markdown Pipeline

A local, resilient Python pipeline designed to convert PDF documents into structured Markdown format. This tool optimizes documents for Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) architectures by drastically reducing token consumption and preserving critical structural data like tables.

## Key Features

* **Token Optimization:** Converts raw PDF text into clean Markdown, reducing visual noise and lowering token costs significantly.
* **Structural Integrity:** Preserves tables and formatting to prevent AI hallucinations during RAG workflows.
* **Local Processing:** Runs entirely on your machine without requiring external API keys.
* **Modular Design:** Built with a fault-tolerant, object-oriented architecture utilizing Microsoft's `markitdown` engine.

## Usage

**Batch Processing:**
1. Place your target `.pdf`, `.docx`, or `.xlsx` files into the `data/input_files` directory.
2. Execute the main script:
    ```bash
    python main.py
    ```
3. Retrieve your processed `.md` files from the `data/output_md` directory.

This pipeline is powered by the [MarkItDown](https://github.com/microsoft/markitdown) engine developed by Microsoft. Our architecture wraps this core parsing engine into a fault-tolerant, batch-processing pipeline suitable for automated AI data preparation workflows.
