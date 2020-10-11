import os
import sys
import json
import pkg_resources
from subprocess import call
import subprocess

from pkg_resources import get_distribution



class PipUpgrade:
    def __init__(self):
        self.packages = [dist.project_name for dist in pkg_resources.working_set]
        self.packages.remove('pip')

        self.importance_list = ['~=', '!=', '>=', '<', '==']
        self.importance_list = ['==', '~=', '<', '>=']

        self.len = len(self.packages)
        
        self.dict = self.create_dict(self.packages)

        self.outdated = self.check_outdated()

    def create_dict(self, packages):
        return {x: [] for x in packages}

    def check_outdated(self):
        print('Checking outdated packages...')
        reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'list', '--format=json', '--outdated'])
        reqs = reqs.decode("utf-8").replace("\r\n", "")     # fix here
        
        outdated = json.loads(reqs)     # List
        return outdated

    # Dependencies

    def get_dependencies(self):
        """
            The main func for getting dependencies and comparing them to output a final list
        """

        self._getDependencies()

        be_upgraded = {}

        for pkg_dict in self.outdated:
            pkg_name = pkg_dict['name']
            current_version = pkg_dict['version']
            latest_version = pkg_dict['latest_version']

            deps = self.dict[pkg_name]

            apply_dep = self.compare_deps(deps, latest_version)

            be_upgraded[pkg_name] = apply_dep

        return be_upgraded

        # self.upgrade(be_upgraded)        

    def compare_deps(self, deps, latest_version):
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
                    raise Exception
                else:
                    return store


    def _getDependencies(self):
        for pkg_test in self.packages:

            dep_list = get_distribution(pkg_test)._dep_map
            dep_list = dep_list.get(None)

            for i in dep_list:
                name = i.key        # Name of dependency
                specs = i.specs     # Specs of dependency

                try:
                    if len(self.dict[name]) > 0:
                        self.dict[name].append(specs)
                    else:
                        self.dict[name] = specs
                except:
                    print(f'There is a problem with package {name}')

    # Upgrade
    
    def upgrade(self, be_upgraded):
        packages = []
        for key, value in be_upgraded.items():
            if not value:
                packages.append(key)
                pkg = key
            else:
                packages.append(key + value[0][0] + value[0][1])
                pkg = key + value[0][0] + value[0][1]

            call("pip install -U " + pkg, shell=True)
        
        packages = " ".join(str(x) for x in packages)
        
        # call("pip install -U " + packages, shell=True)
            
    
    
    # Useful tools for warnings

    def name_check(self, name):
        """
            Package and dependencie name sometimes can't be matched because of upper lower case.
            - Pass these packages, and give a warning for now. TODO find a better solution
        """
        try:
            self.dict[name]
        except:
            print(f'There is a problem with package {name}')
            