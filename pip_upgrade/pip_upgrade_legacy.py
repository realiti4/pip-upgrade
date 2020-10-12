"""
    An old template version of the tool. It can be used by pip-upgrade-legacy but it is not recommended. This will be deleted.
"""

import os
import pkg_resources
from subprocess import call

from pkg_resources import get_distribution


def legacy():
    packages = [dist.project_name for dist in pkg_resources.working_set]
    packages.remove('pip')

    # call("pip install --upgrade " + ' '.join(packages), shell=True)

    main_pkg = 'gym'
    dep = {}

    for pkg_test in packages:

        test = get_distribution(pkg_test)._dep_map
        dep_list = test.get(None)

        temp = []

        for i in dep_list:
            name = i.key
            specs = i.specs

            temp.append([name, specs])

        dep[pkg_test] = temp

    final_dep_dict = {}

    def check_if_needed(item):
        for dep_i in item[1]:
            if dep_i[0] == '>=':
                pass
            else:
                final_dep_dict[item[0]] = dep_i

    for key, value in dep.items():
        if not len(value) == 0:
            for item in value:
                if not len(item[1]) == 0:
                    if item[0] in final_dep_dict:

                        for dep_i in item[1]:
                            if not dep_i[0] == '>=':
                            
                                # TODO compare which one is lower

                                stored_version = final_dep_dict[item[0]]

                                if not dep_i == stored_version:
                                    if dep_i[0] == stored_version[0]:
                                        stricker_version = dep_i[1] if dep_i[1] < stored_version[1] else stored_version[1]
                                        new_value = (dep_i[0], stricker_version)

                                        final_dep_dict[item[0]] = new_value
                                    else:   
                                        # TODO select what to do if symbol is different
                                        print('TODO select best option')
                                        if '<' in dep_i:
                                            final_dep_dict[item[0]] = dep_i
                                        elif '<' in stored_version:
                                            pass
                                        else:                                    
                                            raise Exception('TODO select best option')
                                
                    else:
                        check_if_needed(item)

    # for i, pkg in enumerate(packages):
    #     if pkg in final_dep_dict:
    #         packages[i] = pkg+final_dep_dict[pkg][0]+final_dep_dict[pkg][1]

    call("pip freeze > temp_current.txt", shell=True)

    with open('temp_current.txt', 'r') as f:
        lines = f.readlines()

        with open('temp_target.txt', 'w') as save_file:

            for line in lines:
                line = line.splitlines()[0]
                if '==' in line:
                    split = line.split('==')
                    name = split[0]
                    version = split[1]

                    if name in final_dep_dict:
                        dep_value = final_dep_dict[name]
                        line = name+final_dep_dict[name][0]+final_dep_dict[name][1]+'\n'
                        save_file.write(line)

                    else:
                        line = name+'>='+version+'\n'
                        save_file.write(line)

        
    call("pip install -r temp_target.txt --upgrade", shell=True)

    os.remove('temp_current.txt')
    os.remove('temp_target.txt')
