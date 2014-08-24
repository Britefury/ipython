import sys

if sys.platform.startswith('java'):
    from org.zeromq import ZMQ

    class Context (ZMQ.Context):
        __instance = None


        def __init__(self, num_io_threads):
            super(Context, self).__init__(num_io_threads)

        @classmethod
        def instance(cls):
            if cls.__instance is None:
                cls.__instance = cls(1)
            return cls.__instance



else:
    from zmq import Context
