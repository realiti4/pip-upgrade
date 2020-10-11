import os
import sys
import json
import pkg_resources
from subprocess import call
import subprocess

from pkg_resources import get_distribution

from pip_upgrade.version_checker import version_check

from pip._vendor import pkg_resources

"""
    TODO
    - check if virtualenv is active
    - don't upgrade locally installed packages
    - further testing is needed
"""

class PipUpgrade:
    def __init__(self):
        self.packages = [dist.project_name for dist in pkg_resources.working_set]
        self.packages.remove('pip')

        # self.packages = self.get_packages()
        # self.packages.remove('pip')        

        self.importance_list = ['==', '~=', '<', '<=', '>', '>=', '!=']

        self.len = len(self.packages)
        
        self.dict = self.create_dict(self.packages)

        self.outdated = self.check_outdated()

    # Packages info
    
    def get_packages(self):
        packages = subprocess.check_output([sys.executable, '-m', 'pip', 'list', '--format=json'])
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
        return outdated

    def create_dict(self, packages):
        return {x: [] for x in packages}

    # Dependencies

    def get_dependencies(self):
        """
            The main func for getting dependencies and comparing them to output a final list
        """

        self.retrieve_dependencies()

        be_upgraded = {}
        self.wont_upgrade = []

        for pkg_dict in self.outdated:
            pkg_name = pkg_dict['name']
            current_version = pkg_dict['version']
            latest_version = pkg_dict['latest_version']

            deps = self.dict[pkg_name]

            apply_dep = self.compare_deps(pkg_name, deps, latest_version)

            be_upgraded[pkg_name] = apply_dep

            # TODO Check if it can be upgraded
            if len(apply_dep) > 0:
                version_ = apply_dep[0][1]
                sign_ = apply_dep[0][0]
                if not version_check(apply_dep[0][1], latest_version, apply_dep[0][0]):
                    self.wont_upgrade.append(pkg_name + sign_ + version_)

        return be_upgraded

    def compare_deps(self, pkg_name, deps, latest_version):
        """
            Compares dependencies in a list and decides what packages' final version should be
        """
        store = []
        done = False
        
        for i in self.importance_list:
            for index, i_dep in enumerate(deps):
                sign, version = i_dep

                # for i in self.importance_list:
                if sign == i:
                    store.append([sign, version])
                    done = True
                    # return store

            if done:
                if len(store) > 1:
                    print('TODO')
                    raise Exception('TODO - This will be improved, please try pip-upgrade-legacy for now')
                else:
                    return store
        return store

    def retrieve_dependencies(self):
        for pkg_main in self.packages:

            try:
                dep_list = pkg_resources.working_set.by_key[pkg_main].requires()
            except:
                dep_list = pkg_resources.working_set.by_key[pkg_main.lower()].requires()

            for i in dep_list:
                name = i.name        # Name of dependency
                specs = i.specs     # Specs of dependency
                
                if len(specs) != 0:
                    try:
                        if len(self.dict[name]) > 0:
                            self.dict[name].append(specs)
                        else:
                            self.dict[name] = specs
                    except:
                        print(f'Skipping {name}, warning: Name mismatch. This will be improved. Manually upgrade if needed')

    # Upgrade

    def clear_list(self, packages):
        for item in self.wont_upgrade:
            if item in packages:
                packages.remove(item)
        return packages
    
    def upgrade(self, be_upgraded):
        packages = []
        for key, value in be_upgraded.items():
            if not value:
                packages.append(key)
                pkg = key
            else:
                packages.append(key + value[0][0] + value[0][1])
                pkg = key + value[0][0] + value[0][1]

        packages = self.clear_list(packages)

        if len(packages) > 0:
            # User input
            print(f'These packages will be upgraded: {packages}')
            cont_upgrade = input('Continue? (y/n): ')
            if cont_upgrade.lower() == 'y':
                cont_upgrade = True
            elif cont_upgrade.lower() == 'n':
                cont_upgrade = False
            else:
                raise Exception
            
            if cont_upgrade:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-U', *packages])

        print('All packages are up to date! 🎉')    
            