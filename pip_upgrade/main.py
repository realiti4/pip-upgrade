import sys
import argparse
import logging
from importlib.metadata import version, PackageNotFoundError

from pip_upgrade.tool import PipUpgrade
from pip_upgrade.tools import Config, cprint, clear_cache


def _get_version() -> str:
    try:
        return version("pip-upgrade-tool")
    except PackageNotFoundError:
        return "unknown (not installed)"


parser = argparse.ArgumentParser(
    prog="pip-upgrade",
    description="An easy tool for upgrading all of your packages while not breaking dependencies"
)
parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {_get_version()}")
parser.add_argument("-e", "--exclude", nargs="+", help="Exclude packages you don't want to upgrade")
parser.add_argument("--local", action="store_true", help="Upgrades local packages as well")
parser.add_argument("--novenv", action="store_true", help="Disables venv check")
parser.add_argument("--clear", action="store_true", help="Clears pip's cache")  # Deprecated
parser.add_argument("--clean", action="store_true", help="Clears pip's cache")
parser.add_argument("-y", "--yes", action="store_true", help="Accept all upgrades and skip user prompt")
parser.add_argument("--reset-config", action="store_true", help="Reset config file to default")
parser.add_argument("--dev", action="store_true", help="Doesn't actually call upgrade at the end")
parser.add_argument("--no-cache", action="store_true", help="Disable Redis cache in dev mode")
parser.add_argument("-q", "--query", help="Query package dependency info from pypi")
parser.add_argument("--respect-extras", action="store_true",
    help="Respect ALL version constraints from optional dependencies (extras). "
         "More restrictive than the default heuristic detection.")
parser.add_argument("--no-extras", action="store_true",
    help="Skip all extra-marked dependencies. "
         "By default, extras are detected heuristically by checking if their dependencies are installed.")

args = parser.parse_args()


def check_venv(config):
    """
    Checks if virtualenv is active, throws an asssertion error if not
    """
    if not args.novenv and config["conf"]["novenv"] == "false":
        assert not sys.prefix == sys.base_prefix, (
            "Please use pip-upgrade in a virtualenv. If you would like to surpass this use pip-upgrade --novenv"
        )


def main(dev=False):
    config = Config()

    if dev:
        print("Developer Mode")
        args.dev = True

    if args.reset_config:
        config._reset()
        sys.exit()

    check_venv(config)

    if args.clear or args.clean:
        return clear_cache()

    pip_upgrade = PipUpgrade(args, config)

    try:
        pip_upgrade.get_dependencies()
        pip_upgrade.upgrade()
    except BaseException:
        logging.exception("An exception was thrown!")

        # Print upgrade info if there available upgrades after an exception
        if pip_upgrade.self_check:
            cprint("\nThere is an upgrade for pip-upgrade-tool!", color="green")
            cprint(
                "Please first manually upgrade the tool using 'python -m pip install -U pip-upgrade-tool'\nIf this doesn't fix your issue, please consider opening an issue at https://github.com/realiti4/pip-upgrade",
                disabled=True,
            )


if __name__ == "__main__":
    main(dev=False)
