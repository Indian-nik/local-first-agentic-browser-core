#!/usr/bin/env python3
"""CyberCore v5.0 - Main CLI Application

Ethical Hacking & Penetration Testing Framework
"""
import click
import sys
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

console = Console()

@click.group()
@click.version_option(version="5.0.0", prog_name="CyberCore")
@click.pass_context
def cli(ctx):
    """🔒 CyberCore v5.0 - Elite Ethical Hacking Framework
    
    Quantum-Enhanced Penetration Testing with AI-Powered Intelligence
    
    Built with ❤️ by the CyberCore Security Team
    Empowering ethical hackers worldwide since 2020
    """
    ctx.ensure_object(dict)
    
    # Display banner on first run
    if ctx.invoked_subcommand is None:
        display_banner()

def display_banner():
    """Display CyberCore ASCII banner"""
    banner = r"""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ██████╗██╗   ██╗██████╗ ███████╗██████╗  ██████╗ ██████╗ ███████╗
    ║  ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔═══██╗██╔════╝
    ║  ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║     ██║   ██║█████╗  
    ║  ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║     ██║   ██║██╔══╝  
    ║  ╚██████╗   ██║   ██████╔╝███████╗██║  ██║╚██████╗╚██████╔╝███████╗
    ║   ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
    ║                                                           ║
    ║                    🔒 Version 5.0.0 🔒                     ║
    ║          Elite Ethical Hacking & Penetration Testing      ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")
    console.print("
[yellow]⚠️  AUTHORIZATION REQUIRED - Ethical Use Only ⚠️[/yellow]
")

# Import subcommands
from .commands import (
    scan, exploit, report, quantum, autonomous,
    threat_intel, auth, config
)

# Register commands
cli.add_command(scan.scan)
cli.add_command(exploit.exploit)
cli.add_command(report.report)
cli.add_command(quantum.quantum)
cli.add_command(autonomous.autonomous)
cli.add_command(threat_intel.threat_intel)
cli.add_command(auth.auth)
cli.add_command(config.config)

if __name__ == "__main__":
    cli(obj={})
