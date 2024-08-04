from pkg_resources import working_set

from pip_upgrade.packages import Package, PackageSet
from pip_upgrade.repositories.pypi_repository import PyPiRepository

from poetry.console.commands.update import UpdateCommand
from packaging.utils import canonicalize_name


def get_installed_packages() -> list[Package]:
    installed_packages = PackageSet.from_working_set(working_set)

    installed_packages = [i for i in working_set]

    print("debug")

    installed_packages = [
        Package(
            package.project_name,
            package.version,
            package.location,
            package.key,
            package.precedence,
        )
        for package in installed_packages
    ]

    return installed_packages


def main() -> None:
    repo = PyPiRepository()

    installed_packages = get_installed_packages()

    print("debug")

    # package_info = repo.get_package_info("matplotlib")
    # package_info = repo._find_packages("matplotlib", "1.1")

    # last_version = package_info["versions"][-1]

    # # we can get required_dist from here
    # test = repo._get_release_info("matplotlib", last_version)

    print("Done")


if __name__ == "__main__":
    main()
