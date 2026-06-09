import logging
from pathlib import Path
from typing import List, Optional, Set
from .converter import BaseDocumentConverter, ConversionError

logger = logging.getLogger(__name__)

class DocumentPipeline:
    SUPPORTED_EXTENSIONS: Set[str] = {".pdf", ".docx", ".xlsx"}

    def __init__(self, converter: BaseDocumentConverter, output_dir: Path):
        self.converter = converter
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def process_single(self, file_path: Path) -> Optional[Path]:
        if not file_path.exists() or file_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            logger.error(f"Unsupported or missing file format: {file_path}")
            return None

        try:
            md_content = self.converter.convert(file_path)
            out_path = self.output_dir / f"{file_path.stem}.md"
            out_path.write_text(md_content, encoding='utf-8')
            logger.info(f"Successfully processed: {file_path.name}")
            return out_path
        except ConversionError as ce:
            logger.error(f"Conversion error for {file_path.name}: {ce}")
            return None

    def process_batch(self, input_dir: Path) -> List[Path]:
        successful_paths = []
        for file_path in input_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                result = self.process_single(file_path)
                if result:
                    successful_paths.append(result)
        return successful_paths