import sys

"""backport a few patches from newer pyzmq

These can be removed as we bump our minimum pyzmq version
"""

import zmq

if sys.platform.startswith('java'):
    import json

    def dumps(o, **kwargs):
        """Serialize object to JSON bytes (utf-8).

        See jsonapi.jsonmod.dumps for details on kwargs.
        """

        if 'separators' not in kwargs:
            kwargs['separators'] = (',', ':')

        s = json.dumps(o, **kwargs)

        if isinstance(s, unicode):
            s = s.encode('utf8')

        return s

    def loads(s, **kwargs):
        """Load object from JSON bytes (utf-8).

        See jsonapi.jsonmod.loads for details on kwargs.
        """

        if str is unicode and isinstance(s, bytes):
            s = s.decode('utf8')

        return json.loads(s, **kwargs)
else:
    import zmq.utils.jsonapi
    if zmq.utils.jsonapi.jsonmod.__name__ == 'jsonlib':
        import json
        zmq.utils.jsonapi.jsonmod = json
    from zmq.utils.jsonapi import *
