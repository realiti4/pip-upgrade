import os
import sys
import json
import subprocess

from pip_upgrade.dependencies_base import DependenciesBase
from pip_upgrade.tools import cprint


class PipUpgrade(DependenciesBase):
    def __init__(self, args, config):
        super(PipUpgrade, self).__init__()
        self.args = args
        self.config = config
        self.colored = '\033[32m' if config['conf']['disable_colors'] == 'false' else '\033[m'
        self.restorable = False
        if 'restore' in config.config:
            if len(config['restore']['last_exclude']) != 0:
                self.restorable = True

        # Exclude editable and user defined packages
        self.excluded_pkgs = [] if self.args.exclude is None else self.args.exclude
        self.excluded_pkgs += self.config['conf']['exclude'].split(' ')
        if not self.args.local:     # Exclude editable packages
            self.excluded_pkgs = self.get_packages(args=['--editable']) + self.excluded_pkgs

        self.outdated = self.check_outdated()

    # Packages info

    def get_packages(self, args=[]):
        """
            This gets packages from pip, but it might be slower. Maybe use this later.
        """
        arg_list = [sys.executable, '-m', 'pip', 'list', '--format=json'] + args

        packages = subprocess.check_output(arg_list)
        packages = packages.decode("utf-8").replace("\n", "")
        packages = json.loads(packages)

        packages_list = []

        for pkg in packages:
            packages_list.append(pkg['name'])

        return packages_list

    def check_outdated(self):
        print('Checking outdated packages...')
        reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'list', '--format=json', '--outdated'])
        reqs = reqs.decode("utf-8").replace("\n", "").replace("\r", "")     # fix here

        outdated = json.loads(reqs)     # List

        # Exclude package itself
        for i, item in enumerate(outdated):
            if item['name'] == 'pip-upgrade-tool':
                self.self_check = True
                outdated.pop(i)

        # Exclude other packages
        # print(f'Excluding locally installed packages: {self.excluded_pkgs}')
        outdated_return = []
        for i, item in enumerate(outdated):
            if not item['name'] in self.excluded_pkgs:
                outdated_return.append(item)

        return outdated_return

    # Upgrade

    def clear_list(self, main, subtract, check_input_error=False):
        """
            Removes subtract's elements from main
        """
        for item in subtract:
            if item in main:
                main.pop(item)
            else:
                if check_input_error:
                    raise Exception(f'{item} is not in upgradable packages. This error is for safety incase of typos')
        return main

    def user_prompt(self, packages):
        if self.args.yes:
            cont_upgrade = 'y'
        else:
            cont_upgrade = input('Continue? (y/n or -e/-r/--help): ')

        if cont_upgrade.lower() == 'y':
            cont_upgrade = True
            self.config['restore']['last_exclude'] = ""
            self.config._save()
        elif cont_upgrade.lower() == 'n':
            cont_upgrade = False
        elif cont_upgrade.startswith('-e'):
            exclude = cont_upgrade.split(" ")
            exclude.remove('-e')
            self.clear_list(packages, exclude, check_input_error=True)
            cont_upgrade = True if len(packages) > 0 else False
            self.config['restore']['last_exclude'] = " ".join(str(x) for x in exclude)
            self.config._save()
        elif cont_upgrade.lower() == '-r' or cont_upgrade.lower() == '--repeat':
            if self.restorable:
                repeat = self.config['restore']['last_exclude']
                
                exclude = repeat.split(" ")
                self.clear_list(packages, exclude, check_input_error=False)
                cont_upgrade = True if len(packages) > 0 else False
            else:
                print('No previous setting to repeat...')
                cont_upgrade = self.user_prompt(packages)
        elif cont_upgrade.lower() == '-h' or cont_upgrade.lower() == '--help':
            self._help()
            cont_upgrade = self.user_prompt(packages)
        else:
            print('Please use one of the accepted inputs (y/n or -e PackageNames)\nCanceling...')
            cont_upgrade = False

        return cont_upgrade
    
    def upgrade(self):
        be_upgraded = self.be_upgraded
        packages = {}
        for name, value in be_upgraded.items():
            if not value:
                packages[name] = ''
                pkg = name
            else:
                packages[name] = value[0] + value[1]

        packages = self.clear_list(packages, self.wont_upgrade)

        if len(packages) > 0:
            # Info
            cprint('These packages will be upgraded: ', list(packages.keys()), color='green')
            if self.restorable:
                restore = self.config['restore']['last_exclude']
                print(f'(-r, --repeat  :  -e {restore})')
            
            # User input
            cont_upgrade = self.user_prompt(packages)

            # Prepare packages dict
            packages = list(packages.items())
            packages = [''.join(x) for x in packages]

            if cont_upgrade and not self.args.dev:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-U', *packages])

        print('All packages are up to date! 🎉')

        if self.self_check:
            print("A new update avaliable for pip-upgrade-tool.\nPlease manually upgrade the tool using 'python -m pip install -U pip-upgrade-tool'")
            # cprint("A new update avaliable for pip-upgrade-tool.\nPlease manually upgrade the tool using 'python -m pip install -U pip-upgrade-tool'", color='yellow')

    def _help(self):
        print("")
        print("y              :  Continue")
        print("n              :  Abort")
        print("-e, --exclude  :  Exclude packages and continue. Example: -e pytest hypothesis")
        print("-r, --repeat   :  Repeat previous excluded pkgs")
        print("")
