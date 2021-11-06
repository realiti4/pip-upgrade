import configparser
import os


class Config(configparser.ConfigParser):
    def __init__(self):
        self.home = os.path.expanduser('~')
        self.name = '.pipupgrade.ini'
        self.config = configparser.ConfigParser()

        self.defaults = {
            'conf': {
                'exclude': '',
                'noenv': 'false',
            },
            'restore': {}
        }

        self._init()

    def _save(self):
        with open(os.path.join(self.home, self.name), 'w') as f:
            self.config.write(f)

    def _read(self):
        self.config.read(os.path.join(self.home, self.name))
        if not self._check_validity:
            print('something')  # do something
    
    def _init(self):
        if not os.path.isfile(os.path.join(self.home, self.name)):
            # Conf
            self.config.add_section('conf')
            self.config['conf']['exclude'] = ''
            self.config['conf']['novenv'] = 'false'
            self.config['conf']['max_cache'] = 'false'
            self.config['conf']['disable_colors'] = 'false'
            # Restore
            self.config.add_section('restore')
            self.config['restore']['last_exclude'] = ''
            # Save
            self._save()
        else:
            self._read()

    def _check_validity(self):
        # Check config validity
        # TODO Check missing keys efficiently
        if not self.config.has_section('conf'):
            print("Invalid config (no `conf` section), config will be ignored.")
            self.config.add_section('conf')
            self.config['conf']['novenv'] = 'false'
            self.config['conf']['exclude'] = ''
        if not self.config.has_option('conf', 'novenv'):
            self.config['conf']['novenv'] = 'false'
        if not self.config.has_option('conf', 'exclude'):
            self.config['conf']['exclude'] = ''

    def _reset(self):
        if input("Are you sure you want to completely reset the config file? (y/n): ") == 'y':
            if os.path.isfile(os.path.join(self.home, self.name)):
                os.remove(os.path.join(self.home, self.name))
                self.config = configparser.ConfigParser()
                self._init()
        else:
            print('Aborted, not resetting config.')
    
    def __getitem__(self, key):
        return self.config[key]

    def __repr__(self):
        return self.config