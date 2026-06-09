import logging
from pathlib import Path
from doc2md import MicrosoftMarkItDownConverter, DocumentPipeline

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    INPUT_DIRECTORY = Path("./data/input_files")
    OUTPUT_DIRECTORY = Path("./data/output_md")
    
    INPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    
    converter_engine = MicrosoftMarkItDownConverter()
    pipeline = DocumentPipeline(converter=converter_engine, output_dir=OUTPUT_DIRECTORY)
    
    pipeline.process_batch(INPUT_DIRECTORY)