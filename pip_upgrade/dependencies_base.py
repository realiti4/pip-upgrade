from pip._vendor import pkg_resources
from pip_upgrade.version_checker import version_check, not_equal_check
from pip_upgrade.store import Store


class DependenciesBase:
    def __init__(self):
        self.self_check = False

        self.packages = [dist.project_name for dist in pkg_resources.working_set]
        self.be_upgraded = {}
        self.wont_upgrade = {}
        
        self.dict = self.create_dict(self.packages)
        self.outdated = None
    
    def create_dict(self, packages):
        """
            Creates a dict of Stores class for packages
        """
        return {x: Store(x) for x in packages}

    def get_dependencies(self):
        """
            The main func for getting dependencies and comparing them to output a final list
        """

        self.retrieve_dependencies()        

        for pkg_dict in self.outdated:
            pkg_name = pkg_dict['name']
            current_version = pkg_dict['version']
            latest_version = pkg_dict['latest_version']

            try:
                pkg_store = self.dict[pkg_name]
            except:
                try:
                    pkg_store = self.dict[pkg_name.lower()]
                except Exception as e:
                    if '_' in pkg_name:     # Fix for '_'
                        pkg_name = pkg_name.replace('_', '-')
                    try:
                        pkg_store = self.dict[pkg_name]
                    except Exception as e:
                        raise e
            
            pkg_store.current_version = current_version
            pkg_store.latest_version = latest_version

            self.compare_deps(pkg_store)

    def compare_deps(self, pkg_store):
        """
            Compares dependencies in a list and decides what packages' final version should be
        """
        result = []
        done = False
        
        for key in ['==', '~=', '<', '<=']:                
            if len(pkg_store.data[key]) > 0:
                result = [key, min(pkg_store.data[key])]
                done = True
                break
        if not done:
            for key in ['>', '>=']:
                if len(pkg_store.data[key]) > 0:
                    result = [key, max(pkg_store.data[key])]
                    done = True
                    break
            #  Nonequal Check
            for item in pkg_store.data['!=']:
                not_equal_check(item, pkg_store.latest_version)
                result = ['!=', pkg_store.latest_version]

        if version_check(result, pkg_store.latest_version):
            self.be_upgraded[pkg_store.name] = result

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
                        self.dict[name] += specs
                    except:
                        for key in self.dict:
                            if key.lower() == name.lower():
                                name = key
                        try:                            
                            self.dict[name] += specs
                        except Exception as e:
                            if '_' in name:     # Fix for '_'
                                name = name.replace('_', '-')
                            try:
                                self.dict[name] += specs
                            except Exception as e:
                                # raise e
                                print(f'Skipping {name}, warning: Name mismatch. This will be improved. Manually upgrade if needed')

    def check_name_in_dict(self):
        """
            Case and '_', '-' checks. Returns the true name on dict
        """
        return
