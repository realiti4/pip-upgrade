

from tool import PipUpgrade



def main():
    pip_upgrade = PipUpgrade()

    be_upgraded = pip_upgrade.get_dependencies()
    
    pip_upgrade.upgrade(be_upgraded)




main()