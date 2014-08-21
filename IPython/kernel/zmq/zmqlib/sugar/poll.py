import os

if os.name == 'java':
    """0MQ polling related functions and classes."""

    # Copyright (C) PyZMQ Developers
    # Distributed under the terms of the Modified BSD License.
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
    from org.zeromq import ZMQ

    class Poller(object):
        """A stateful poll interface that mirrors Python's built-in poll."""

        def __init__(self):
            self.__poller = ZMQ.Poller(32)
            self.__sockets = set()

        def __contains__(self, socket):
            return socket in self.__sockets

        def register(self, socket, flags=ZMQ_POLLIN|ZMQ_POLLOUT):
            """p.register(socket, flags=POLLIN|POLLOUT)

            Register a 0MQ socket or native fd for I/O monitoring.

            register(s,0) is equivalent to unregister(s).

            Parameters
            ----------
            socket : zmq.Socket or native socket
                A zmq.Socket or any Python object having a ``fileno()``
                method that returns a valid file descriptor.
            flags : int
                The events to watch for.  Can be POLLIN, POLLOUT or POLLIN|POLLOUT.
                If `flags=0`, socket will be unregistered.
            """
            # print 'zmqlib.sugar.poll.Poller.register: socket type = {0}'.format(type(socket))
            if flags == 0:
                self.__poller.unregister(socket)
                self.__sockets.remove(socket)
            else:
                self.__poller.register(socket, flags)
                self.__sockets.add(socket)

        def modify(self, socket, flags=ZMQ_POLLIN|ZMQ_POLLOUT):
            """Modify the flags for an already registered 0MQ socket or native fd."""
            self.register(socket, flags)

        def unregister(self, socket):
            self.__poller.unregister(socket)
            self.__sockets.remove(socket)

        def poll(self, timeout=None):
            """Poll the registered 0MQ or native fds for I/O.

            Parameters
            ----------
            timeout : float, int
                The timeout in milliseconds. If None, no `timeout` (infinite). This
                is in milliseconds to be compatible with ``select.poll()``. The
                underlying zmq_poll uses microseconds and we convert to that in
                this function.

            Returns
            -------
            events : list of tuples
                The list of events that are ready to be processed.
                This is a list of tuples of the form ``(socket, event)``, where the 0MQ Socket
                or integer fd is the first element, and the poll event mask (POLLIN, POLLOUT) is the second.
                It is common to call ``events = dict(poller.poll())``,
                which turns the list of tuples into a mapping of ``socket : event``.
            """
            if timeout is None or timeout < 0:
                timeout = -1
            elif isinstance(timeout, float):
                timeout = int(timeout)
            n_events = self.__poller.poll(timeout)
            events = []
            if n_events > 0:
                for i in xrange(self.__poller.getSize()):
                    item = self.__poller.getItem(i)
                    ops = item.readyOps()
                    if ops > 0:
                        events.append((item.getSocket(), ops))
            return events

    def select(rlist, wlist, xlist, timeout=None):
        """select(rlist, wlist, xlist, timeout=None) -> (rlist, wlist, xlist)

        Return the result of poll as a lists of sockets ready for r/w/exception.

        This has the same interface as Python's built-in ``select.select()`` function.

        Parameters
        ----------
        timeout : float, int, optional
            The timeout in seconds. If None, no timeout (infinite). This is in seconds to be
            compatible with ``select.select()``. The underlying zmq_poll uses microseconds
            and we convert to that in this function.
        rlist : list of sockets/FDs
            sockets/FDs to be polled for read events
        wlist : list of sockets/FDs
            sockets/FDs to be polled for write events
        xlist : list of sockets/FDs
            sockets/FDs to be polled for error events

        Returns
        -------
        (rlist, wlist, xlist) : tuple of lists of sockets (length 3)
            Lists correspond to sockets available for read/write/error events respectively.
        """
        if timeout is None:
            timeout = -1
        # Convert from sec -> us for zmq_poll.
        # zmq_poll accepts 3.x style timeout in ms
        timeout = int(timeout*1000.0)
        if timeout < 0:
            timeout = -1
        sockets = []
        for s in set(rlist + wlist + xlist):
            flags = 0
            if s in rlist:
                flags |= ZMQ_POLLIN
            if s in wlist:
                flags |= ZMQ_POLLOUT
            if s in xlist:
                flags |= ZMQ_POLLERR
            sockets.append(PollItem(s, flags))
        return_sockets = ZMQ.zmq_poll(sockets, timeout)
        rlist, wlist, xlist = [], [], []
        for s, flags in return_sockets:
            if flags & ZMQ_POLLIN:
                rlist.append(s)
            if flags & ZMQ_POLLOUT:
                wlist.append(s)
            if flags & ZMQ_POLLERR:
                xlist.append(s)
        return rlist, wlist, xlist

    #-----------------------------------------------------------------------------
    # Symbols to export
    #-----------------------------------------------------------------------------

    __all__ = [ 'Poller', 'select' ]
else:
    from zmq import Poller, select
