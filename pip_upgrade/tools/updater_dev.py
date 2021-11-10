import subprocess
import sys

def spawn_program_and_die(program, exit_code=0):
    """
    Start an external program and exit the script 
    with the specified return code.

    Takes the parameter program, which is a list 
    that corresponds to the argv of your command.
    """
    # Start the external program
    subprocess.Popen(program)
    # We have started the program, and can suspend this interpreter
    sys.exit(exit_code)

spawn_program_and_die(['python', 'path/to/my/script.py'])

# Or, as in OP's example
spawn_program_and_die(['python', 'file2.py'])