from .common import Waker as _Waker


def set_close_exec(fd):
    """Sets the close-on-exec bit (``FD_CLOEXEC``)for a file descriptor.

    According to:

    http://stackoverflow.com/questions/8997643/launch-a-child-process-from-java-that-doesnt-inherit-files-ports-on-unix

    Java does this by default, so its not necessary here?
    """
    pass


class Waker (_Waker):
    def fileno(self):
        return self.reader.fileno().channel

