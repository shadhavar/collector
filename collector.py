import os
import sys
import socket
import json

if not __name__ == "__main__":
    print "The collector should not be imported as a module"
    os.exit(1)

# Load config
print "Loading config"
f = open("config", "r")
conf = json.loads(f.read())
socketpath = conf["socketpath"]

# create a unix domain socket to be used as sink
print "Preparing domain socket"
sink = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
try:
    os.remove(socketpath)
except:
    pass

sink.bind(socketpath)

# Prepare modules and plugins
modules = {}
plugins = {}
for name, values in conf["plugins"].iteritems():
    k = values["plugin"]
    if not k in modules:
        print "Importing {0}".format(k)
        modules[k] = getattr(__import__('plugins.{0}'.format(k), globals(), locals(), [k], -1), k)

    print "Initializing {0}".format(name)
    plugins[name] = modules[k](socketpath, values)

#TODO see if stuff gets lost when starting takes a while
for name, instance in plugins.iteritems():
    print "Starting {0}".format(name)
    instance.start()

try:
    while True:
        data, address = sink.recvfrom(4096) # hmm
        print >>sys.stderr, data
except:
    print "Shutting down"
    for name, instance in plugins.iteritems():
        print "Stopping {0}".format(name)
        instance.shutdown = True
    sink.close()
