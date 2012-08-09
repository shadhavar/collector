from plugin import Plugin
import time

class Dummy(Plugin):
    Name = "Dummy"
    Description = "Dummy plugin sending a silly message every second"

    def __init__(self, socketpath, config):
        Plugin.__init__(self, socketpath, config)
        self.message = config['message']

    #TODO see if we can wrap this shutdown logic
    def run(self):
        while not self.shutdown:
            self.send(self.message)
            time.sleep(1)
        self.socket.close()
