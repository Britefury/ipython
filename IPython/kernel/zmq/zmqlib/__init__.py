import sys

from .sugar import MessageTracker
from .error import *
from .context import *


if sys.platform.startswith('java'):
    from zmq.ZMQ import \
        ZMQ_NOBLOCK, \
        ZMQ_POLLIN, \
        ZMQ_POLLOUT, \
        ZMQ_POLLERR, \
        ZMQ_REQ, \
        ZMQ_SUB, \
        ZMQ_DEALER, \
        ZMQ_SUBSCRIBE, \
        ZMQ_IDENTITY
    from zmq import Poller
    from zmq.ZError import ETERM as ZMQ_ETERM, EAGAIN as ZMQ_EAGAIN
else:
    from zmq import \
        ETERM as ZMQ_ETERM, \
        EAGAIN as ZMQ_EAGAIN, \
        NOBLOCK as ZMQ_NOBLOCK, \
        POLLIN as ZMQ_POLLIN, \
        POLLOUT as ZMQ_POLLOUT, \
        POLLERR as ZMQ_POLLERR, \
        REQ as ZMQ_REQ, \
        SUB as ZMQ_SUB, \
        DEALER as ZMQ_DEALER, \
        SUBSCRIBE as ZMQ_SUBSCRIBE, \
        IDENTITY as ZMQ_IDENTITY
    from zmq import Poller, Socket
