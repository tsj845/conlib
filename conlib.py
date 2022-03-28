import sys
import os
import tty
import termios
from typing import Tuple, Union, Callable, Any

def set_raw_decorator (func : Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    decorates a function by setting the terminal to raw mode, then reverting it after the decorated function has completed
    """
    def ret (*args, **kwargs):
        fileno : int = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fileno)
        res : Union[Any, None] = None
        try:
            tty.setraw(fileno)
            res = func(*args, **kwargs)
        finally:
            termios.tcsetattr(fileno, termios.TCSADRAIN, old_settings)
            print("\x1b[1G", end="")
        return res
    return ret

def _readin_to_char (char : str) -> str:
    """
    reads sys.stdin until "char" is reached, note that this shouldn't be used to read actual user input
    """
    f : str = ""
    while True:
        f += sys.stdin.read(1)
        if f[-1] == char:
            break
    return f

@set_raw_decorator
def getcurpos () -> Tuple[int, int]:
    """
    gets the cursor's current position in the format (x, y)
    """
    print("\x1b[6n", sep="", end="", flush=True)
    text : str = _readin_to_char("R")
    x : int = int(text[2:text.index(";")])
    y : int = int(text[text.index(";")+1:text.index("R")])
    return (x, y)

@set_raw_decorator
def getchar (show_entered : bool = True) -> str:
    """
    reads a character from sys.stdin
    """
    c : str = sys.stdin.read(1)
    if c == "\x1b":
        c2 : str = sys.stdin.read(1)
        while not c2.isalpha():
            c += c2
            c2 = sys.stdin.read(1)
        c += c2
    if show_entered:
        print(c, sep="", end="", flush=True)
    return c

def get_size () -> Tuple[int, int]:
    """
    returns the current terminal size in the format (columns, rows)
    """
    sizing = os.get_terminal_size()
    return (sizing.columns, sizing.lines)

def getchars (n : int = 1, show_entered_chars : bool = True) -> str:
    """
    gets the requested number of characters
    """
    chars : str= ""
    for i in range(n):
        chars += getchar(show_entered_chars)
    return chars

@set_raw_decorator
def readin (prompt : str = "", *, show_entered_chars : bool = True, replace_chars_with : Union[str, None] = None) -> str:
    """
    returns user input
    """
    print(prompt, sep="", end="", flush=True)
    f : str = ""
    global log
    while True:
        c : str = sys.stdin.read(1).replace("\r", "\n")
        if show_entered_chars:
            print(c if replace_chars_with == None or c == "\n" else replace_chars_with, sep="", end="", flush=True)
        if c in "\x03\x04":
            raise KeyboardInterrupt()
        if c == "\n":
            break
        f += c
    return f

def clear ():
    print("\x1bc", sep="", end="", flush=True)