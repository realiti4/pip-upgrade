import sys
import subprocess
import shutil
import argparse
import configparser
import os

from pip_upgrade.tool import PipUpgrade

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--exclude', nargs='+', help="Exclude packages you don't want to upgrade")
parser.add_argument('--local', action='store_true', help="Upgrades local packages as well")
parser.add_argument('--novenv', action='store_true', help="Disables venv check")
parser.add_argument('--clear', action='store_true', help="Clears pip's cache")
parser.add_argument('--reset-config', action='store_true', help='Reset config file to default')
parser.add_argument('-q', '--query', help="Query package dependency info from pypi")

args = parser.parse_args()

def get_config():
    """
        Make config if it doesn't already exist and read it into the `config` variable. Then ensure config validity
    """
    home = os.path.expanduser("~")
    config = configparser.ConfigParser()
    if not os.path.isfile(os.path.join(home, ".pipupgrade.ini")):
        config.add_section('conf')
        config['conf']['exclude'] = ''
        config['conf']['novenv'] = 'false'
        with open(os.path.join(home, '.pipupgrade.ini'), 'w') as f:
            config.write(f)
    else:
        config.read(os.path.join(home, '.pipupgrade.ini'))

    # Check config validity
    if not config.has_section('conf'):
        print("Invalid config (no `conf` section), config will be ignored.")
        config.add_section('conf')
        config['conf']['novenv'] = 'false'
        config['conf']['exclude'] = ''
    if not config.has_option('conf', 'novenv'):
        config['conf']['novenv'] = 'false'
    if not config.has_option('conf', 'exclude'):
        config['conf']['exclude'] = ''

    return config

def reset_config():
    if input("Are you sure you want to completely reset the config file? (y/n): ") == 'y':
        home = os.path.expanduser("~")
        if os.path.isfile(os.path.join(home, '.pipupgrade.ini')):
            os.remove(os.path.join(home, '.pipupgrade.ini'))
    else:
        print('Aborted, not resetting config.')
    return get_config()

def check_venv(config):
    """
        Checks if virtualenv is active, throws an asssertion error if not
    """
    if not args.novenv and config['conf']['novenv'] == 'false':
        assert not sys.prefix == sys.base_prefix, 'Please use pip-upgrade in a virtualenv. If you would like to surpass this use pip-upgrade --novenv'

def clear_cache():
    """
        Clears pip cache
    """
    arg_list = [sys.executable, '-m', 'pip', 'cache', 'dir']
    output = subprocess.check_output(arg_list)
    output = output.decode("utf-8").replace("\n", "").replace("\r", "")

    print(f'Folder will be deleted: {output}')
    confirm = input('Continue? (y/n): ')

    if confirm.lower() == 'y':
        try:
            shutil.rmtree(output)
            print('Cache is cleared..')
        except Exception as e:
            print(e)
    else:
        print('Aborted, if the folder was wrong, please fill an issue.')

def main():
    config = get_config()

    if args.reset_config:
        config = reset_config()

    check_venv(config)

    if args.clear:
        return clear_cache()

    pip_upgrade = PipUpgrade(args, config)

    be_upgraded = pip_upgrade.get_dependencies()

    pip_upgrade.upgrade(be_upgraded)

if __name__ == "__main__":
    main()
