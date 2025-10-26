"""Threat Intelligence Command"""
import click
from rich.console import Console

console = Console()

@click.group()
def threat_intel():
    """Threat intelligence operations"""
    pass

@threat_intel.command()
@click.argument('indicator')
def lookup(indicator):
    """Lookup threat intelligence"""
    console.print(f"[yellow]Looking up: {indicator}[/yellow]")
