import sys

if sys.platform.startswith('java'):
    class ZMQStream (object):
        pass


else:
    from zmq.eventloop.zmqstream import *

