# pip-upgrade
The purpose of pip-upgrade is to be a simple yet robust and reliable tool for upgrading all of your packages while not breaking dependencies

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

**Tip:** You can use `-e` to exclude packages in `Continue? (y/n):` after seeing which packages are going to be upgraded. This is super useful for packages like gohlke's Numpy+mkl for example.
```
These packages will be upgraded: ['hypothesis', 'Pillow', 'pytest', 'setuptools']
Continue? (y/n): -e pytest hypothesis
```

You can also exclude packages beforehand. Use `-e` or `--exclude`. The tool won't upgrade dependency breaking packages already, this is extra for packages that you want to keep it at a version.

    $ pip-upgrade -e numpy pandas
### Options
- `pip-upgrade -e` Exclude packages you don't want to upgrade. Can take multiple or single value.
- `pip-upgrade --clear` Clear pip's cache.
- `pip-upgrade --local`	By default locally installed editable packages (installed with `pip install . -e`) won't be upgraded. Use this option to upgrade everything.
- `pip-upgrade --novenv` By default the tool won't work if virtualenv is not active. Use this if you want use it globally and pass the assertion error.

#### TODO / known issues
- Bug - Doesn't detect != cases if * is used (!=5.4.*)
- Feature - Update directly from Gohlke's packages
