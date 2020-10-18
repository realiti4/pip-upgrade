# pip-box
The purpose of pip-box is to be a simple yet robust and reliable tool for upgrading all of your packages while not breaking dependencies

## Installation

	pip install pip-box
	
or	

    git clone https://github.com/realiti4/pip-box.git
    cd pip-box
    pip install .

## Usage
Just run `pip-box` in your terminal while virtualenv is active.

    $ pip-box

If there are packages you want to exclude use `-e` or `--exclude`. The tool won't upgrade dependency breaking packages already, this is extra for packages that you want to keep it at a version.

    $ pip-box -e numpy pandas

```
Checking outdated packages...
These packages will be upgraded: ['colorama', 'isort']
Continue? (y/n): y
All packages are up to date! 🎉
```

**Tip:** You can use `-e` to exclude packages in `Continue? (y/n):` after seeing which packages are going to be upgraded.
```
These packages will be upgraded: ['hypothesis', 'Pillow', 'pytest', 'setuptools']
Continue? (y/n): -e pytest hypothesis
```
### Options
- `pip-box -e` Exclude packages you don't want to upgrade. Can take multiple or single value.
- `pip-box --local`	By default locally installed editable packages (installed with `pip install . -e`) won't be upgraded. Use this option to upgrade everything.
- `pip-box --novenv` By default the tool won't work if virtualenv is not active. Use this if you want use it globally and pass the assertion error.

#### TODO - known issues
- Feature - Query dependency informations of a package from pypi servers.
