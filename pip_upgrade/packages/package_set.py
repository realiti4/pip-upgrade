
from typing import Self

from .package import Package


class PackageSet:
    def __init__(self, packages: list[Package]):
        self.working_set = packages

    @classmethod 
    def from_working_set(cls, working_set) -> Self:
        installed_packages = [
            Package(
                package.project_name,
                package.version,
                package.location,
                package.key,
                package.precedence,
            )
            for package in working_set
        ]

        return cls(installed_packages)
        
    def __iter__(self):
        return iter(self.working_set)

    def __len__(self):
        return len(self.working_set)

    # def __getitem__(self, name):
    #     return self.working_set[name]

    # def get_by_key(self, key):
    #     return self._package_by_key[key]

    # def get_by_filename(self, filename):
    #     return self._package_by_file[filename]

    # def keys(self):
    #     return self.working_set.keys()

    # def items(self):
    #     return self.working_set.items()

    # def values(self):
    #     return self.working_set.values()

    # def __contains__(self, name):
    #     return name in self.working_set

    # def __eq__(self, other):
    #     return self.working_set == other._package_by_name

    # def __ne__(self, other):
    #     return self.working_set != other._package_by_name

    # def difference(self, other):
    #     return PackageSet(set(self.values()) - set(other.values()))

    # def intersection(self, other):
    #     return PackageSet(set(self.values()) & set(other.values()))

    # def union(self, other):
    #     return PackageSet(set(self.values()) | set(other.values()))

    # def __repr__(self):
    #     return "<PackageSet({})>".format(self.working_set)

    # def __hash__(self):
    #     return hash(self.working_set)
