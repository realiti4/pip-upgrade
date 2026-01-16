from importlib.metadata import distribution, distributions
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

from pip_upgrade.version_checker import version_check, not_equal_check
from pip_upgrade.store import Store


class DependenciesBase:
    def __init__(self, respect_extras=False):
        self.respect_extras = respect_extras
        self.self_check = False

        self.packages = [dist.metadata['Name'] for dist in distributions()]
        self.be_upgraded = {}
        self.wont_upgrade = {}

        self.dict = self.create_dict(self.packages)
        self.outdated = None

    def create_dict(self, packages):
        """
        Creates a dict of Stores class for packages
        """
        return {canonicalize_name(x): Store(x) for x in packages}

    def get_dependencies(self):
        """
        The main func for getting dependencies and comparing them to output a final list
        """

        self.retrieve_dependencies()

        for pkg_dict in self.outdated:
            pkg_name = pkg_dict["name"]
            current_version = pkg_dict["version"]
            latest_version = pkg_dict["latest_version"]

            pkg_store = self.dict[canonicalize_name(pkg_name)]

            pkg_store.current_version = current_version
            pkg_store.latest_version = latest_version

            self.compare_deps(pkg_store)

    def compare_deps(self, pkg_store):
        """
        Compares dependencies in a list and decides what packages' final version should be
        """
        result = []
        done = False

        for key in ["==", "~=", "<", "<="]:
            if len(pkg_store.data[key]) > 0:
                result = [key, min(pkg_store.data[key])]
                done = True
                break
        if not done:
            for key in [">", ">="]:
                if len(pkg_store.data[key]) > 0:
                    result = [key, max(pkg_store.data[key])]
                    done = True
                    break
            #  Nonequal Check
            for item in pkg_store.data["!="]:
                not_equal_check(item, pkg_store.latest_version)
                result = ["!=", pkg_store.latest_version]

        if version_check(result, pkg_store.latest_version):
            self.be_upgraded[pkg_store.name] = result

    def retrieve_dependencies(self):
        """
        Retrieves dependencies pkg_main requires, and puts all dependent packages in self.dict with their version.
        """
        for pkg_main in self.packages:
            dist = distribution(pkg_main)
            requires = dist.requires or []

            for req_str in requires:
                req = Requirement(req_str)
                name = req.name
                canonical_name = canonicalize_name(name)

                # Skip if package not installed
                if canonical_name not in self.dict:
                    continue

                # Skip if no version specifier
                if len(req.specifier) == 0:
                    continue

                # Check marker (handles python_version, extras, etc.)
                if req.marker:
                    # Check if this is an extra-only marker (e.g., extra == "all")
                    marker_str = str(req.marker)
                    is_extra_marker = 'extra' in marker_str

                    if is_extra_marker:
                        if not self.respect_extras:
                            # Skip extra-marked dependencies by default - we can't determine
                            # if the extra is actually installed, and optional dependencies
                            # shouldn't block upgrades
                            continue
                        # If respect_extras=True, fall through and apply the constraint
                    else:
                        # For python_version, platform, etc: evaluate against current env
                        if not req.marker.evaluate():
                            continue

                # Add version constraints
                for spec in req.specifier:
                    self.dict[canonical_name] += [(spec.operator, spec.version)]

