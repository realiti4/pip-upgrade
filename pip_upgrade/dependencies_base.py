from pip._vendor import pkg_resources
from pip_upgrade.version_checker import version_check, min_dependency

"""
    TODO 
    - Create a dependency matrix which will make searching much more easy
    - Update dep values by getting new info from pypi servers
"""


class DependenciesBase:
    def __init__(self):
        self.self_check = False

        self.packages = [dist.project_name for dist in pkg_resources.working_set]
        # self.packages.remove('pip')

        # self.packages = self.get_packages()
        # self.packages.remove('pip')
        
        self.dict = self.create_dict(self.packages)
        self.outdated = None

        self.importance_list = ['==', '~=', '<', '<=', '>', '>=', '!=']    
    
    def build_dep_matrix(self):
        """
            - One hot encoding for every package and use numpy or use pandas' indexes if we can search by name
        """
        raise NotImplementedError 

    def get_dependencies(self):
        """
            The main func for getting dependencies and comparing them to output a final list
        """

        self.retrieve_dependencies()

        be_upgraded = {}
        self.wont_upgrade = {}

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
                    self.wont_upgrade[pkg_name] = sign_ + version_

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
                    # TODO check if taking min always is the right thing here
                    return [min_dependency(store)]
                else:
                    return store
        return store

    def retrieve_dependencies(self):
        """
            Retrieves dependencies pkg_main requires, and puts all dependent packages in self.dict with their version.
        """
        for pkg_main in self.packages:

            try:
                dep_list = pkg_resources.working_set.by_key[pkg_main].requires()
            except:
                dep_list = pkg_resources.working_set.by_key[pkg_main.lower()].requires()

            for i in dep_list:
                name = i.name        # Name of dependency
                specs = i.specs      # Specs of dependency
                
                if len(specs) != 0:
                    try:
                        if len(self.dict[name]) > 0:
                            self.dict[name].append(specs[0])
                        else:
                            self.dict[name] = specs
                    except:
                        for key in self.dict:
                            if key.lower() == name.lower():
                                # print(name, key)
                                name = key
                        try:                            
                            self.dict[name] = specs
                        # if name == 'pillow':    # TODO fix lower case completely
                        #    self.dict['Pillow'] = specs
                        except:
                            print(f'Skipping {name}, warning: Name mismatch. This will be improved. Manually upgrade if needed')

    def create_dict(self, packages):
        return {x: [] for x in packages}
