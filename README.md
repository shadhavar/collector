# collector

## About
The collector is the data harvesting client of shadhavar.

It currently depends on python (2.6 and later) and optionally on
[py-setproctitle](http://code.google.com/p/py-setproctitle/).

## Features
* Configuration is loaded from files on the machine running the collector, but a remote server can push
changes as well. Files will be parsed using [confuse](http://www.nongnu.org/confuse/)
* Data will be collected by simple plugins, running in seperate processes.
* Planned plugins
    * Files
    * Sockets
    * Commands (both continously running and returning programs)
* No parsing keeps the collector light
* Messages are sent to the server using [zeromq](http://zeromq.org/)

## Status
* The basic plugin infrastructure has been implemented
* Configuration uses json at the moment, only `$PWD/config` is read. Global options:
    * socketpath: string; path to the socket used for communication with plugins
* Implemented plugins and their config options:
    * Dummy: Sends the same message every second
        * message: string; literal string sent to the collector
    * UDS: Reads unix domain sockets, useful for e.g. syslog
        * listen: boolean; indicates whether the socket should be bound or not
        * path: string; path to the socket
        * type: string; socket type, "DGRAM" for datagram, "STREAM" for stream
