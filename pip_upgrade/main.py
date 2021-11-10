import sys
import subprocess
import shutil
import argparse

from pathlib import Path
from pip_upgrade.tool import PipUpgrade
from pip_upgrade.tools import Config

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--exclude', nargs='+', help="Exclude packages you don't want to upgrade")
parser.add_argument('--local', action='store_true', help="Upgrades local packages as well")
parser.add_argument('--novenv', action='store_true', help="Disables venv check")
parser.add_argument('--clear', action='store_true', help="Clears pip's cache")  # Deprecated
parser.add_argument('--clean', action='store_true', help="Clears pip's cache")
parser.add_argument('-y', '--yes', action='store_true', help="Accept all upgrades and skip user prompt")
parser.add_argument('--reset-config', action='store_true', help='Reset config file to default')
parser.add_argument('--dev', action='store_true', help="Doesn't actually call upgrade at the end")
parser.add_argument('-q', '--query', help="Query package dependency info from pypi")

args = parser.parse_args()



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

    # Dev - print folder size
    dev_path = Path(output)
    cache_size = sum(f.stat().st_size for f in dev_path.glob('**/*') if f.is_file())
    cache_size = int((cache_size / 1024) / 1024)

    print(f'Folder will be deleted: {output}  Size: {cache_size}MB')
    confirm = input('Continue? (y/n): ')

    if confirm.lower() == 'y':
        try:
            shutil.rmtree(output)
            print('Cache is cleared..')
        except Exception as e:
            print(e)
    else:
        print('Aborted, if the folder was wrong, please fill an issue.')

def main(dev=False):
    config = Config()

    if dev:
        print('Developer Mode')
        args.dev = True

    if args.reset_config:
        config._reset()
        sys.exit()

    check_venv(config)

    if args.clear or args.clean:
        return clear_cache()

    pip_upgrade = PipUpgrade(args, config)

    pip_upgrade.get_dependencies()

    pip_upgrade.upgrade()

if __name__ == "__main__":
    main(dev=False)
