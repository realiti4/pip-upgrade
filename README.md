# pip-upgrade
The purpose of pip-upgrade is to be a simple yet rebost and reliable tool for upgrading all of your packages while not breaking dependencies

## Installation

	pip install pip-upgrade-tool
	
or	

    git clone https://github.com/realiti4/pip-upgrade.git
    cd pip-upgrade
    pip install .

## Usage
Just run `pip-upgrade` in your terminal while virtualenv is active.

    $ pip-upgrade

```
Checking outdated packages...
All packages are up to date! 🎉
```

### Options
- `pip-upgrade --local`	By default locally installed editable packages (installed with `pip install . -e`) won't be upgraded. Use this option to upgrade everything.
- `pip-upgrade --novenv` By default the tool won't work if virtualenv is not active. Use this if you want use it globally and pass the assertion error.

#### TODO - known issues
- With some packages, there might be name check errors, because of dependency and package name case differences. Tool skips these and gives a warning for now. I only run into Pillow so far, and there is a manual fix for that. There might be other packages, this will be improved.
