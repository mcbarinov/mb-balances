"""CLI entry point for mb-balances."""

import importlib.metadata
from pathlib import Path
from typing import Annotated

import typer
from mm_clikit import print_toml

from mb_balances.config import Config

app = typer.Typer(no_args_is_help=True, pretty_exceptions_enable=False)

_EXAMPLE_CONFIG = Path(__file__).parent / "example.toml"


@app.command()
def main(
    config: Annotated[Path | None, typer.Argument(help="Path to config file.")] = None,
    version: Annotated[bool, typer.Option("--version", "-V", is_eager=True, help="Print version and exit.")] = False,
    example: Annotated[bool, typer.Option("--example", is_eager=True, help="Print example config and exit.")] = False,
) -> None:
    """Fetch crypto balances from a TOML config and display totals."""
    if version:
        typer.echo(f"mb-balances {importlib.metadata.version('mb-balances')}")
        raise typer.Exit

    if example:
        print_toml(_EXAMPLE_CONFIG.read_text())
        raise typer.Exit

    if config is None:
        raise typer.BadParameter("Missing argument 'CONFIG'.")

    cfg = Config.load_or_exit(config)
    cfg.print_and_exit()
