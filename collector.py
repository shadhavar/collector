import os
import sys
import socket
import json
import subprocess
import signal

def signal_main(signum, frame):
    print "Shutting down"
    for name, process in processes.iteritems():
        print "Stopping {0}".format(name)
        process.terminate()
    sink.close()
    exit(0)

def signal_plugin(signum, frame):
    global m
    print "Exiting plugin {0}".format(sys.argv[1])
    m.shutdown = True

def load_config():
    print "Loading config"
    f = open("config", "r")
    conf = json.loads(f.read())
    f.close()
    return conf

def run_plugin(instance):
    global m
    if not instance in conf["plugins"]:
        print "No configuration for {0}, exiting.".format(name)
        os.exit(1)

    values = conf["plugins"][instance]

    print "Importing {0}".format(values["plugin"])
    modulename = values["plugin"]
    module = getattr(__import__('plugins.{0}'.format(modulename), globals(), locals(), [modulename], -1), modulename)
    m = module(socketpath, values)

    signal.signal(signal.SIGTERM, signal_plugin)

    print "Starting plugin {0}".format(instance)
    while not m.shutdown:
       m.run()
    m.stop()


# create a unix domain socket to be used as sink
def initialize_socket():
    print "Preparing domain socket"
    sink = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        os.remove(socketpath)
    except:
        pass

    sink.bind(socketpath)
    return sink


if __name__ == "__main__":
    conf = load_config()
    socketpath = conf["socketpath"]

    # if passed an argument, we run that plugin instance
    if len(sys.argv) > 1:
        run_plugin(sys.argv[1])
    else:
        sink = initialize_socket()

        # Prepare modules and plugins
        processes = {}
        #TODO see if stuff gets lost when starting takes a while
        for name in conf["plugins"].keys():
            print "Starting collector for plugin {0}".format(name)
            processes[name] = subprocess.Popen([sys.executable, sys.argv[0], name])

        #TODO regularly poll() the subprocesses

        signal.signal(signal.SIGTERM, signal_main)

        while True:
            data, address = sink.recvfrom(4096) # hmm
            print >>sys.stderr, data
