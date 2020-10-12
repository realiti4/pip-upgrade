# pip-upgrade
The purpose of pip-upgrade is to be a simple yet rebost and reliable tool for upgrading all of your packages while not breaking dependencies

## Installation

	pip install pip-upgrade-tool
	
or	

    git clone https://github.com/realiti4/pip-upgrade.git
    cd pip-upgrade
    pip install .

## Usage
#### version 0.3.7
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
- With some packages, there might be name check errors, because of dependency and package name case differences. Tools skips these and gives a warning for now. This will be improved.
