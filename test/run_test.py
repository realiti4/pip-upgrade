import pytest
import argparse

from pip_upgrade.tool import PipUpgrade
from pip_upgrade.utils.config import Config


parser = argparse.ArgumentParser()
parser.add_argument('-e', '--exclude', nargs='+', help="Exclude packages you don't want to upgrade")
parser.add_argument('--local', action='store_true', help="Upgrades local packages as well")
parser.add_argument('--novenv', action='store_true', help="Disables venv check")
parser.add_argument('--clear', action='store_true', help="Clears pip's cache")  # Deprecated
parser.add_argument('--clean', action='store_true', help="Clears pip's cache")
parser.add_argument('-y', '--yes', action='store_true', help="Accept all upgrades and skip user prompt")
parser.add_argument('--reset-config', action='store_true', help='Reset config file to default')
parser.add_argument('--dev', action='store_true', help="Doesn't actually call upgrade at the end")

args = parser.parse_args()

def test_main():
    config = Config()

    args.dev = True
    args.yes = True

    pip_upgrade = PipUpgrade(args, config)

    pip_upgrade.get_dependencies()

    pip_upgrade.upgrade()

