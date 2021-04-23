from packaging import version


def version_check(dep, latest_version):
    if len(dep) == 0:
        return True

    sign_dict = {'==': 0, '~=': 1, '<': 2, '<=': 3, '>': 4, '>=': 5, '!=': 6}

    sign, apply_dep = dep
    key = sign_dict[sign]

    if key == 0:
        result = version.parse(apply_dep) == version.parse(latest_version)
    elif key == 1:
        result = version.parse(apply_dep).minor == version.parse(latest_version).minor
    elif key == 2:
        result = version.parse(latest_version) < version.parse(apply_dep)
    elif key == 3:
        result = version.parse(latest_version) <= version.parse(apply_dep)
    elif key == 4:
        result = version.parse(latest_version) > version.parse(apply_dep)
    elif key == 5:
        result = version.parse(latest_version) >= version.parse(apply_dep)
    elif key == 6:
        result = version.parse(latest_version) != version.parse(apply_dep)
    else:
        print(f'version check error: {sign}')

    return result
    
def not_equal_check(version_, latest_version):

    # if any(['!=' in x for x in deps]):
    #     for dep in deps:
    #         _sign = dep[0]
    #         _version = dep[1]
    #         if _sign == '!=':
    if '.*' in version_:
        version_, _ = version_.split('.*')

    if latest_version[:len(version_)] == version_:
        return True
    else:
        return False    

def min_dependency(deps):
    """
        Gets min of two version
    """
    deps_list = []

    for dep in deps:
        _sign = dep[0]
        _version = dep[1]
        deps_list.append(version.parse(_version))

    return [_sign, str(min(deps_list))]
