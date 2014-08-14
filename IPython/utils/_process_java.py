"""Java-specific implementation of process utilities, loosely based on _process_cli

This file is only meant to be imported by process.py, not by end-users.

This file is largely untested. To become a full drop-in process
interface for IronPython will probably require you to help fill
in the details. 
"""

from __future__ import print_function

# Import java.lang.System
from java.lang import System

# Import Python libraries:
import os
import sys

from subprocess import STDOUT

# Import IPython libraries:
from IPython.utils import py3compat
from ._process_common import arg_split

from ._process_common import read_no_interrupt, process_handler, arg_split as py_arg_split
from . import py3compat
from .encoding import DEFAULT_ENCODING



def _find_cmd(cmd):
    """Find the full path to a command using which."""
    paths = System.getenv('PATH').split(os.pathsep)
    for path in paths:
        filename = os.path.join(path, cmd)
        if os.path.exists(filename):
            return py3compat.bytes_to_str(filename)
    raise OSError("command %r not found" % cmd)


def system(cmd):
    os.system(cmd)


def getoutput(cmd):
    out = process_handler(cmd, lambda p: p.communicate()[0], STDOUT)

    if out is None:
        out = b''
    return py3compat.bytes_to_str(out)