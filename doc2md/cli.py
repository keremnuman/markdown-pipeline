import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pydub")

import logging
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import track

from .converter import get_converter
from .pipeline import DocumentPipeline
from .config import PipelineConfig

app = typer.Typer(
    name="doc2md",
    help="Convert PDF, DOCX, XLSX files to Markdown — fast and scriptable.",
    add_completion=False,
)
console = Console()


@app.command()
def convert(
    input_path: Path = typer.Argument(
        None,
        help="Input file or directory. Overrides config file.",
    ),
    output_dir: Path = typer.Option(
        None,
        "--output", "-o",
        help="Output directory. Overrides config file.",
    ),
    config_path: Path = typer.Option(
        Path("config.yaml"),
        "--config", "-c",
        help="Path to config.yaml.",
    ),
    workers: int = typer.Option(
        None,
        "--workers", "-w",
        help="Parallel worker count. Overrides config file.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Show detailed logs.",
    ),
):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.WARNING)
    cfg = PipelineConfig.from_yaml_if_exists(config_path)
    if input_path:
        cfg.input_dir = input_path
    if output_dir:
        cfg.output_dir = output_dir
    if workers:
        cfg.max_workers = workers

    if not cfg.input_dir.exists():
        console.print(f"[red]Input path does not exist: {cfg.input_dir}[/red]")
        raise typer.Exit(1)

    converter  = get_converter(cfg.converter)
    pipeline   = DocumentPipeline(
        converter=converter,
        output_dir=cfg.output_dir,
        max_workers=cfg.max_workers,
    )

    if cfg.input_dir.is_file():
        files = [cfg.input_dir]
    else:
        files = [
            f for f in cfg.input_dir.iterdir()
            if f.is_file() and f.suffix.lower() in cfg.supported_extensions
        ]

    if not files:
        console.print("[yellow]No supported files found.[/yellow]")
        raise typer.Exit()

    results = []
    for f in track(files, description="Converting..."):
        result = pipeline.process_single(f)
        results.append((f.name, result))

    table = Table(title="Conversion Results", show_lines=True)
    table.add_column("File", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Output")

    success_count = 0
    for name, result in results:
        if result:
            table.add_row(name, "[green]✓[/green]", str(result))
            success_count += 1
        else:
            table.add_row(name, "[red]✗[/red]", "—")

    console.print(table)
    console.print(
        f"\n[bold]{success_count}/{len(results)}[/bold] files converted "
        f"→ [cyan]{cfg.output_dir}[/cyan]"
    )


def main():
    app()