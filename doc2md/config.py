from dataclasses import dataclass, field
from pathlib import Path
from typing import Set
import yaml


@dataclass
class PipelineConfig:
    input_dir: Path = Path("./data/input_files")
    output_dir: Path = Path("./data/output_md")
    max_workers: int = 4
    converter: str = "markitdown"
    supported_extensions: Set[str] = field(
        default_factory=lambda: {".pdf", ".docx", ".xlsx"}
    )

    @classmethod
    def from_yaml(cls, path: Path) -> "PipelineConfig":
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        return cls(
            input_dir=Path(data.get("input_dir", "./data/input_files")),
            output_dir=Path(data.get("output_dir", "./data/output_md")),
            max_workers=int(data.get("max_workers", 4)),
            converter=data.get("converter", "markitdown"),
            supported_extensions=set(
                data.get("supported_extensions", [".pdf", ".docx", ".xlsx"])
            ),
        )

    @classmethod
    def from_yaml_if_exists(cls, path: Path) -> "PipelineConfig":
        if path.exists():
            return cls.from_yaml(path)
        return cls()