"""
Main module for configuring CLI commands.

Refer to README.rst for instructions to run commands via the CLI.

:see: https://typer.tiangolo.com/tutorial/subcommands/add-typer/#put-them-together
"""
__all__ = ["app"]

import typer

from cli.commands import generate

app = typer.Typer()

# Activate commands.
app.add_typer(generate.app, name="generate")

if __name__ == "__main__":
    app()
