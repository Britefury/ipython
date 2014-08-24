from . import interface

from org.zeromq import ZMQ
from ....context import Context
import uuid


def set_close_exec(fd):
    """Sets the close-on-exec bit (``FD_CLOEXEC``)for a file descriptor.

    According to:

    http://stackoverflow.com/questions/8997643/launch-a-child-process-from-java-that-doesnt-inherit-files-ports-on-unix

    Java does this by default, so its not necessary here?
    """
    pass


class Waker(interface.Waker):
    """Create an OS independent asynchronous pipe.

    For use on platforms that don't have os.pipe() (or where pipes cannot
    be passed to select()), but do have sockets.  This includes Windows
    and Jython.
    """
    def __init__(self):
        # Based on Zope async.py: http://svn.zope.org/zc.ngi/trunk/src/zc/ngi/async.py

        address = 'inproc://' + str(uuid.uuid4())

        ctx = Context.instance()

        self.writer = ctx.socket(ZMQ.REQ)
        self.writer.bind(address)

        self.reader = ctx.socket(ZMQ.REP)
        self.reader.bind(address)


    def fileno(self):
        return self.reader

    def write_fileno(self):
        return self.writer

    def wake(self):
        try:
            self.writer.send(b"x")
        except IOError:
            pass

    def consume(self):
        try:
            while True:
                result = self.reader.recv()
                if not result:
                    break
        except IOError:
            pass

    def close(self):
        self.reader.close()
        self.writer.close()
