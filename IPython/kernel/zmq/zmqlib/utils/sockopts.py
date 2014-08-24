# ZMQ socket options are set in pyzmq and JeroMQ using slightly different APIs. This module abstracts away these differences.

import os

if os.name == 'java':
    def set_identity(socket, identity):
        return socket.setIdentity(identity)

    def subscribe(socket, topic):
        return socket.subscribe(topic)

    def get_bind_to_random_port_method(socket):
        return socket.bindToRandomPort

else:
    import zmq
    def set_identity(socket, identity):
        return socket.setsockopt(zmq.IDENTITY, identity)

    def subscribe(socket, topic):
        return socket.setsockopt(zmq.SUBSCRIBE, topic)

    def get_bind_to_random_port_method(socket):
        return socket.bind_to_random_port
