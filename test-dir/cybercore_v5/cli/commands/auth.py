"""Authorization Command"""
import click
from rich.console import Console

console = Console()

@click.group()
def auth():
    """Authorization and scope management"""
    pass

@auth.command()
@click.argument('scope_file')
def verify(scope_file):
    """Verify authorization scope"""
    console.print(f"[green]Verifying scope: {scope_file}[/green]")
