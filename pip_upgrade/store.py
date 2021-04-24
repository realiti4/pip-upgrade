from copy import deepcopy
from packaging import version


# class pkgdict:  


class Store:
    def __init__(self, pkg_name: str, current: str = None, latest: str = None):
        self.name = pkg_name
        self.current = current
        self.latest = latest

        self.data = {'==': [], '~=': [], '<': [], '<=': [], '>': [], '>=': [], '!=': []}

        self.ready = False

    def __iadd__(self, item):
        self.add(item)
        return self
    
    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, item):
        assert key in self.data, 'Item is not in keys'
        self.data[key] = item

    def __len__(self):
        return sum([len(self.data[key]) for key in self.data])

    def __repr__(self):
        output = ''
        for key in self.data:
            output += key + ':\n' + '  ' + str(self.data[key]) + '\n'
        return output

    def type_check(self, sign):
        """
            Returns a function to compare version
        """
        if sign in ['==', '~=', '<', '<=']:
            group = 'less'
            return min, group
        elif sign in ['>', '>=']:
            group = 'greater'
            return max, group
        else:
            group = 'nonequal'
            return None, group

    def add(self, item):
        assert isinstance(item, list)
        assert len(item[0]) == 2, 'It only accepts list of (sign, version)'
        for sub_item in item:
            sign_, version_ = sub_item
            self.data[sign_].append(version_)
    
    def add__(self, deps):
        """
            Adds value to store while applying min or max
        """
        assert isinstance(deps, list), 'It takes list of deps [(sign, version), ..]'

        for _sign, _version in deps:
            compare, group = self.type_check(_sign)
            _version = version.parse(_version)

            self.data[group]['sign'].append(_sign)
            self.data[group]['data'].append(_version)

        # if compare is None:     # Nonequal
        #     self.data[group]['sign'] = '!='
        #     self.data[group]['data'] += _version
        # else:
        #     self.data[group]['sign'] = '!='

        print('de')   

    def get(self):
        """
            Runs compare_ and gets final data. It has to be called after all adding is done.
        """
        if not self.ready:  # Disabled, always prepare the data for now
            self.prepare_()
        return self.get_data

    def prepare_(self):
        self.get_data = deepcopy(self.data)
        for key in ['==', '~=', '<', '<=']:
            self.get_data[key] = [min(self.get_data[key])]
        for key in ['>', '>=']:
            self.get_data[key] = [max(self.get_data[key])]
    
    def compare_(self):
        """
            Compares versions when all items are added
        """
        print('Debug: running compare..')
        for key in self.data:
            sign = self.data[key]['sign']
            data = self.data[key]['data']
            func = self.data[key]['compare_func']
            if not len(data) == 0 and func is not None:
                index = data.index(func(data))
                self.data[key]['sign'] = sign[index]
                self.data[key]['data'] = data[index]
        # self.ready = True
    