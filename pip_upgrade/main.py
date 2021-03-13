import sys
import subprocess
import shutil
import argparse

from pip_upgrade.tool import PipUpgrade

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--exclude', nargs='+', help="Exclude packages you don't want to upgrade")
parser.add_argument('--local', action='store_true', help="Upgrades local packages as well")
parser.add_argument('--novenv', action='store_true', help="Disables venv check")
parser.add_argument('--clear', action='store_true', help="Clears pip's cache")
parser.add_argument('-q', '--query', help="Query package dependency info from pypi")

args = parser.parse_args()


def check_venv():
    """
        Checks if virtualenv is active, throws an asssertion error if not
    """
    if not args.novenv:
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
    check_venv()
    
    if args.clear:
        return clear_cache()

    pip_upgrade = PipUpgrade(args)

    be_upgraded = pip_upgrade.get_dependencies()
    
    pip_upgrade.upgrade(be_upgraded)

if __name__ == "__main__":
    main()
