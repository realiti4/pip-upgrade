# pip-upgrade
The purpose of pip-upgrade is to be a simple yet rebost and reliable tool for upgrading all of your packages while not breaking dependencies

## Installation

	pip install pip-upgrade-tool
	
or	

    git clone https://github.com/realiti4/pip-upgrade.git
    cd pip-upgrade
    pip install .

### version 0.3.0
Just run 'pip-upgrade' in your terminal while virtualenv is active.

    $ pip-upgrade
    
#### TODO - known issues
- Gets dependencies in lower case, so skips packages like Pillow and Cython. This'll be improved.

- Add an arg to not upgrade local packapes installed with 'pip install .'

- This should be fixed with 0.3.0 - Let's say x package holding y. They got an update at the same time and now x package requires y at a higher minimum version than it was holding it for. y packege won't be upgraded unless 'pip-upgrade' is run twice.
