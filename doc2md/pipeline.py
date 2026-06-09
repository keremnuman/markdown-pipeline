import logging
from pathlib import Path
from typing import List, Optional, Set
from concurrent.futures import ThreadPoolExecutor, as_completed
from .converter import BaseDocumentConverter, ConversionError

logger = logging.getLogger(__name__)


class DocumentPipeline:
    SUPPORTED_EXTENSIONS: Set[str] = {".pdf", ".docx", ".xlsx"}

    def __init__(
        self,
        converter: BaseDocumentConverter,
        output_dir: Path,
        max_workers: int = 4,
    ):
        self.converter = converter
        self.output_dir = output_dir
        self.max_workers = max_workers
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def process_single(self, file_path: Path) -> Optional[Path]:
        if not file_path.exists() or file_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            logger.error(f"Unsupported or missing file: {file_path}")
            return None
        try:
            md_content = self.converter.convert(file_path)
            out_path = self.output_dir / f"{file_path.stem}.md"
            out_path.write_text(md_content, encoding="utf-8")
            logger.info(f"Successfully processed: {file_path.name}")
            return out_path
        except ConversionError as ce:
            logger.error(f"Conversion error for {file_path.name}: {ce}")
            return None

    def process_batch(self, input_dir: Path) -> List[Path]:
        candidates = [
            f for f in input_dir.iterdir()
            if f.is_file() and f.suffix.lower() in self.SUPPORTED_EXTENSIONS
        ]

        if not candidates:
            logger.warning("No supported files found in directory.")
            return []

        successful_paths = []
        failed_count = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.process_single, f): f for f in candidates}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    successful_paths.append(result)
                else:
                    failed_count += 1

        logger.info(
            f"Batch complete — {len(successful_paths)} successful, "
            f"{failed_count} failed, {len(candidates)} total"
        )
        return successful_paths