collector
=========

== features ==
* Config loaded from config files in /etc
* Config can be changed via config files OR via remote server who pushes changes
* config files via http://www.nongnu.org/confuse/
* Input to send:
** Files
** syslog
** stdout of commands 
** continuous stdout of commands who run 'for ever'
* all input will be send without any parsing (but maybe with extra metadata)to the receiver
* Commands: config options
** Location of the command
** time interval
* continuous commands
** location of the command
* we will leverage the power of the zmq messaging layer.
