# Script courtesy of:
# https://code.activestate.com/recipes/134892/

# Script to read a single character from STDIN
# We are using this to control the robot via the keyboard
# to test the functionality of the motor system.

# This script is not used in any way during normal operation
# of the PiRover

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
     screen."""
    def __init__(self):
        self.impl = _GetchUnix()
    def __call__(self): return self.impl()
class _GetchUnix:
    def __init__(self):
        import tty, sys
    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

getch = _Getch()
