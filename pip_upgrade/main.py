import sys
import argparse

from pip_upgrade.tool import PipUpgrade

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--exclude', nargs='+', help="Exclude packages you don't want to upgrade")
parser.add_argument('--local', action='store_true', help="Upgrades local packages as well")
parser.add_argument('--novenv', action='store_true', help="Disables venv check")
parser.add_argument('-q', '--query', help="Query package dependency info from pypi")

args = parser.parse_args()


def check_venv():
    """
        Checks if virtualenv is active, throws an asssertion error if not
    """
    if not args.novenv:
        assert not sys.prefix == sys.base_prefix, 'Please use pip-upgrade in a virtualenv. If you would like to surpass this use pip-upgrade --novenv'

def main():
    check_venv()

    pip_upgrade = PipUpgrade(args)

    be_upgraded = pip_upgrade.get_dependencies()
    
    pip_upgrade.upgrade(be_upgraded)

if __name__ == "__main__":
    main()
