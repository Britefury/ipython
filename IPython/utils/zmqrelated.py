"""Utilities for checking zmq versions."""
#-----------------------------------------------------------------------------
#  Copyright (C) 2013  The IPython Development Team
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING.txt, distributed as part of this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Verify zmq version dependency >= 2.1.11
#-----------------------------------------------------------------------------

import sys

from IPython.utils.version import check_version



def check_for_zmq(minimum_version, required_by='Someone'):
        try:
            import zmq
        except ImportError:
            raise ImportError("%s requires pyzmq >= %s"%(required_by, minimum_version))

        if sys.platform.startswith('java'):
            from org.zeromq import ZMQ
            pyzmq_version = ZMQ.getVersionString()
        else:
            pyzmq_version = zmq.__version__
    
        if not check_version(pyzmq_version, minimum_version):
            raise ImportError("%s requires pyzmq >= %s, but you have %s"%(
                            required_by, minimum_version, pyzmq_version))

