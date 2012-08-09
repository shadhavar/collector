import threading
import socket

class Plugin(threading.Thread):
    def __init__(self, socketpath, config):
        threading.Thread.__init__(self)
        self.socketpath = socketpath
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.shutdown = False

    def send(self, message):
        if not self.socket:
            return
        self.socket.sendto(message, self.socketpath)

    def run(self):
        raise NotImplementedError("Plugins must implement run()!")
