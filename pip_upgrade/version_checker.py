from packaging import version


# class version_check:
#     def __init__(self):
#         self.sign_dict = ['==', '~=', '<', '<=', '>', '>=', '!=']    

def version_check(apply_dep, latest_version, sign):
    # TODO find a better way
    # TODO check if it is correct

    sign_dict = {'==': 0, '~=': 1, '<': 2, '<=': 3, '>': 4, '>=': 5, '!=': 6}

    key = sign_dict[sign]

    if key == 0:
        result = version.parse(apply_dep) == version.parse(latest_version)
    elif key == 0:  # TODO '~=' what is this?
        result = True
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
    
    



    print('debug')