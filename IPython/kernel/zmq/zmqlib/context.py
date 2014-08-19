import sys

if sys.platform.startswith('java'):
    from org.zeromq import ZContext

    class Context (object):
        __instance = None


        def __init__(self):
            self.__context = ZContext()

        @classmethod
        def instance(cls):
            if cls.__instance is None:
                cls.__instance = Context()
            return cls.__instance


        def socket(self, type):
            return self.__context.createSocket(type)




else:
    from zmq import Context
