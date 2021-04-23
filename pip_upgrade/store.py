from packaging import version


# class pkgdict:  


class Store:
    def __init__(self, pkg_name: str, current: str = None, latest: str = None):
        self.name = pkg_name
        self.current = current
        self.latest = latest

        self.data = {'==': [], '~=': [], '<': [], '<=': [], '>': [], '>=': [], '!=': []}

        # self.data = {
        #     'less': {'sign': [], 'data': [], 'compare_func': min},
        #     'greater': {'sign': [], 'data': [], 'compare_func': max},
        #     'nonequal': {'sign': [], 'data': [], 'compare_func': None},
        # }
        self.ready = False

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

    def add(self, key, item):
        print('de')
    
    def add_(self, deps):
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
        if not self.ready:
            self.prepare_()

    def prepare_(self):
        for key in ['==', '~=', '<', '<=']:
            self.data[key] = [min(self.data[key])]
        for key in ['>', '>=']:
            self.data[key] = [max(self.data[key])]
    
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
        self.ready = True

    def __iadd__(self, item):
        assert isinstance(item, list)
        assert len(item[0]) == 2, 'It only accepts list of (sign, version)'
        for sub_item in item:
            sign_, version_ = sub_item
            self.data[sign_].append(version_)
            # print(f'Debug: {sign_, version_} added..')
        return self
    
    def __getitem__(self, item):
        if not self.ready:
            self.compare_()
        return [[self.data[item]['sign'], str(self.data[item]['data'])]]

    # def __setitem__(self, key, item):
    #     assert key in self.data, 'Item is not in keys'
    #     self.data[key] = item

    def __len__(self):
        return sum([len(self.data[key]['data']) for key in self.data])