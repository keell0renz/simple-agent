"""Launch helpers for Poetry."""

import subprocess
import sys


def main():
    """Launches app normally, not in development mode."""
    try:
        subprocess.run(["chainlit", "run", "./simple_agent/app.py"], check=True)
    except KeyboardInterrupt:
        sys.exit(0)


def dev():
    """Starts development server which updates upon saving."""
    try:
        subprocess.run(["chainlit", "run", "./simple_agent/app.py", "-w"], check=True)
    except KeyboardInterrupt:
        sys.exit(0)
