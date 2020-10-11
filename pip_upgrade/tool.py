import os
import pkg_resources
from subprocess import call

from pkg_resources import get_distribution



class PipUpgrade:
    def __init__(self):
        self.packages = [dist.project_name for dist in pkg_resources.working_set]
        self.packages.remove('pip')

        self.sign_dict = ['~=', '!=', '>=', '<', '==']

        self.len = len(self.packages)
        
        self.dict = self.create_dict(self.packages)        

    def create_dict(self, packages):
        return {x: [] for x in packages}

    # Dependencies

    def get_dependencies(self):
        """
            The main func for getting dependencies and comparing them to output a final list
        """

        self._getDependencies()

        test = []
        
        for key, value in self.dict.items():
            # value = value[0]
            if len(value) > 0:
                test.append(value[0][0])
        
        print(list( dict.fromkeys(test) ))
        print('debug')

    def compare_deps(self):
        """
            Compares dependencies in a list and decides what packages' final version should be
        """
        pass    

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
            