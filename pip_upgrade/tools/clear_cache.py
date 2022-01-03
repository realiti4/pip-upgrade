import sys
import subprocess
import shutil

from pathlib import Path


def clear_cache():
    """
        Clears pip cache
    """
    arg_list = [sys.executable, '-m', 'pip', 'cache', 'dir']
    output = subprocess.check_output(arg_list)
    output = output.decode("utf-8").replace("\n", "").replace("\r", "")

    # Dev - print folder size
    dev_path = Path(output)
    cache_size = sum(f.stat().st_size for f in dev_path.glob('**/*') if f.is_file())
    cache_size = int((cache_size / 1024) / 1024)

    print(f'Folder will be deleted: {output}  Size: {cache_size}MB')
    confirm = input('Continue? (y/n): ')

    if confirm.lower() == 'y':
        try:
            shutil.rmtree(output)
            print('Cache is cleared..')
        except Exception as e:
            print(e)
    else:
        print('Aborted, if the folder was wrong, please fill an issue.')