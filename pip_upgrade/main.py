import sys
import argparse

from pip_upgrade.tool import PipUpgrade

parser = argparse.ArgumentParser()
parser.add_argument('--local', default='CartPole-v0', help='Training environment')
parser.add_argument('--novenv', default='CartPole-v0', help='Training environment')

args = parser.parse_args()


def check_venv():
    """
        Checks if virtualenv is active, throws an asssertion error if not
    """
    assert not sys.prefix == sys.base_prefix, 'Please use pip-upgrade in a virtualenv'

def main():
    check_venv()

    pip_upgrade = PipUpgrade()

    be_upgraded = pip_upgrade.get_dependencies()
    
    pip_upgrade.upgrade(be_upgraded)

if __name__ == "__main__":
    main()