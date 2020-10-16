from packaging import version


def version_check(apply_dep, latest_version, sign):
    # TODO find a better way
    # TODO check if it is correct

    sign_dict = {'==': 0, '~=': 1, '<': 2, '<=': 3, '>': 4, '>=': 5, '!=': 6}

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
