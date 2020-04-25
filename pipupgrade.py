import pkg_resources
from subprocess import call

from pkg_resources import get_distribution




# packages = [dist.project_name for dist in pkg_resources.working_set]
# packages.remove('pip')

# call("pip list --outdated")

# call("pip install --upgrade " + ' '.join(packages), shell=True)

test = get_distribution('botocore')._dep_map
test_list = test.get(None)

for i in test_list:
    name = i.key
    specs = i.specs

    print(test)

print('debugging')