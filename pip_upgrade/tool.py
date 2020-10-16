import os
import sys
import json
from subprocess import call
import subprocess

from pip_upgrade.dependencies_base import DependenciesBase

"""
    TODO
    - further testing is needed
"""

class PipUpgrade(DependenciesBase):
    def __init__(self, args):
        super(PipUpgrade, self).__init__()
        self.args = args        

        # Exclude editable and user defined packages
        self.excluded_pkgs = [] if self.args.exclude is None else self.args.exclude        
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
    
    def upgrade(self, be_upgraded):
        packages = []
        packages = {}
        for name, value in be_upgraded.items():
            if not value:
                packages[name] = ''
                pkg = name
            else:
                packages[name] = value[0][0] + value[0][1]
                pkg = name + value[0][0] + value[0][1]

        packages = self.clear_list(packages, self.wont_upgrade)

        if len(packages) > 0:
            # User input
            print(f'These packages will be upgraded: {list(packages.keys())}')
            cont_upgrade = input('Continue? (y/n): ')
            if cont_upgrade.lower() == 'y':
                cont_upgrade = True
            elif cont_upgrade.lower() == 'n':
                cont_upgrade = False
            elif cont_upgrade.startswith('-e'): # TODO take exclude arg here, test this further
                exclude = cont_upgrade.split(" ")
                exclude.remove('-e')
                self.clear_list(packages, exclude, check_input_error=True)
                cont_upgrade = True if len(packages) > 0 else False
            else:
                print('Please use one of the accepted inputs (y/n or -e PackageNames)\nCanceling...')
                cont_upgrade = False
            
            # Prepare packages dict
            packages = list(packages.items())
            packages = [''.join(x) for x in packages]
            
            if cont_upgrade:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-U', *packages])

        print('All packages are up to date! 🎉')
        
        if self.self_check:
            print("A new update avaliable for pip-upgrade-tool.\nPlease manually upgrade the tool using 'python -m pip install -U pip-upgrade-tool'")
            