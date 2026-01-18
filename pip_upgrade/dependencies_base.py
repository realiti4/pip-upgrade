import re
from importlib.metadata import distribution, distributions
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

from pip_upgrade.version_checker import version_check, not_equal_check
from pip_upgrade.store import Store

from pip._vendor import pkg_resources

class DependenciesBase:
    MIN_DEPS_FOR_HEURISTIC = 2

    def __init__(self, respect_extras=False, no_extras=False):
        self.respect_extras = respect_extras
        self.no_extras = no_extras
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

    def _extract_extra_name(self, marker) -> str | None:
        """Extract extra name from marker like 'extra == "plot"'"""
        match = re.search(r'extra\s*==\s*["\']([^"\']+)["\']', str(marker))
        return match.group(1) if match else None

    def infer_active_extras(self, pkg_name: str) -> set[str]:
        """
        Heuristically determine which extras are likely active.
        An extra is considered active if ALL its optional deps are installed
        and it has at least MIN_DEPS_FOR_HEURISTIC dependencies.
        """
        dist = distribution(pkg_name)
        requires = dist.requires or []

        # Build map: extra_name -> set of required package names
        extras_deps: dict[str, set[str]] = {}

        for req_str in requires:
            req = Requirement(req_str)
            if req.marker and 'extra' in str(req.marker):
                extra_name = self._extract_extra_name(req.marker)
                if extra_name:
                    extras_deps.setdefault(extra_name, set()).add(
                        canonicalize_name(req.name)
                    )

        # Check which extras have ALL their deps installed (with minimum threshold)
        active_extras = set()
        for extra, deps in extras_deps.items():
            if len(deps) >= self.MIN_DEPS_FOR_HEURISTIC and all(dep in self.dict for dep in deps):
                active_extras.add(extra)

        return active_extras

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
        active_extras_cache: dict[str, set[str]] = {}

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
                        if self.respect_extras:
                            # respect_extras=True: apply all extra constraints
                            pass  # Fall through to apply constraint
                        elif self.no_extras:
                            # no_extras=True: skip all extra-marked dependencies
                            continue
                        else:
                            # Default: heuristic check if this extra is likely active
                            if pkg_main not in active_extras_cache:
                                active_extras_cache[pkg_main] = self.infer_active_extras(pkg_main)

                            extra_name = self._extract_extra_name(req.marker)
                            if extra_name not in active_extras_cache[pkg_main]:
                                continue  # Skip - this extra isn't active
                            # Fall through to apply constraint
                    else:
                        # For python_version, platform, etc: evaluate against current env
                        if not req.marker.evaluate():
                            continue

                # Add version constraints
                for spec in req.specifier:
                    self.dict[canonical_name] += [(spec.operator, spec.version)]

