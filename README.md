# pip-upgrade 🎉
The purpose of pip-upgrade is to be a simple yet robust and reliable tool for upgrading all of your packages while not breaking dependencies.

## Installation

	pip install pip-upgrade-tool

or

    pip install git+https://github.com/realiti4/pip-upgrade.git@master --upgrade

## Usage
Just run `pip-upgrade` in your terminal while virtualenv is active.

    $ pip-upgrade

```
Checking outdated packages...
These packages will be upgraded: ['colorama', 'isort']
Continue? (y/n): y
...
All packages are up to date! 🎉
```

**Tip:** You can use `-e` to exclude some packages and continue in `Continue? (y/n):` after seeing which packages are going to be upgraded. This is super useful for packages like gohlke's Numpy+mkl for example. `-r` to repeat the previous excluded packages. It'll show if there is a saved repeatable action.
```
These packages will be upgraded: ['hypothesis', 'Pillow', 'pytest', 'setuptools']
(-r, --repeat  :  -e pytest)
Continue? (y/n or -e/-r/--help): -e pytest hypothesis
```

You can also exclude packages beforehand. Use `-e` or `--exclude`. The tool won't upgrade dependency breaking packages already, this is extra for packages that you want to keep it at a version. You can also add packages to config file for this to persist until you remove. This combined with `pip-upgrade -y` that accepts and skips user prompt can be used for automated environments.

    $ pip-upgrade -e numpy pandas
### Options
- `pip-upgrade -e` Exclude packages you don't want to upgrade. Can take multiple or single value.
- `pip-upgrade -y` Accept all upgrades and skip user prompt.
- `pip-upgrade --clean` Clear pip's cache.
- `pip-upgrade --local`	By default locally installed editable packages (installed with `pip install -e .`) won't be upgraded. Use this option to upgrade everything.
- `pip-upgrade --novenv` By default the tool won't work if virtualenv is not active. Use this if you want use it globally and pass the assertion error.
- `pip-upgrade --reset-config` Reset config file located in `~/.pipupgrade.ini` to it's default.

### Permanent Configuration
When `pip-upgrade` is run for the first time, it will create a file in the user's home directory named `.pipupgrade.ini`. This file can be manually edited by the user for permanent configuration options. The configuration file current consists of two options under the `conf` section, `exclude` and `novenv`. `novenv` is false by default, but if set to true, the `pip-upgrade` command will not require you to be in a virtualenv, which is the same function as the `--novenv` argument. The second option, `exclude`, will take the same values as the `--exclude` argument, but these excluded packages will persist forever until removed. 

### Contributing
Any contribution is appreciated, please feel free to send pull requests.

#### TODO / known issues
- Feature - Update directly from Gohlke's packages
- Feature - Revert to previous point
