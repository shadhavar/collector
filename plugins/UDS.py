from plugin import Plugin
import socket
import os

class UDS(Plugin):
    Name = "Unix Domain Socket"
    Description = "Read unix domain sockets"

    def __init__(self, socketpath, config):
        Plugin.__init__(self, socketpath, config)
        self.listen = config["listen"]
        self.path = config["path"]
        self.socktype = config["type"]
        self.prepare()

    def prepare(self):
        if self.listen: # we are the host
            os.umask(0011)
            try:
                os.remove(self.path)
            except:
                pass

            if self.socktype == "DGRAM":
                self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                self.sock.bind(self.path)
                self.maxrecv = self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF) / 2
            else:
                raise NotImplementedError()
        else:
            raise NotImplementedError()


    def run(self):
        while not self.shutdown:
            data, address = self.sock.recvfrom(self.maxrecv)
            self.send(data)
