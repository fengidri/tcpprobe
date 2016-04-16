# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2016-04-15 01:42:32
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


import argparse
import sys
import signal
import os
import socket
import struct

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--saddr", help="local ip")
parser.add_argument("--daddr", help="remote ip")
parser.add_argument("--sport", help="local port")
parser.add_argument("--dport", help="remote port")
parser.add_argument("-o", help="remote port")
args = parser.parse_args()

class Filter(object):
    def __init__(self):
        self.path = '/proc/net/tcpprobe_filter'
        self.saddr = 0
        self.daddr = 0
        self.sport = 0
        self.dport = 0

    def init(self, args):
        if args.saddr:
            self.set_saddr(args.saddr)

        if args.daddr:
            self.set_daddr(args.daddr)

        if args.sport:
            self.set_sport(args.sport)

        if args.dport:
            self.set_dport(args.dport)

    def set_saddr(self, addr):
        self.saddr = ip_to_int(addr)

    def set_daddr(self, addr):
        self.daddr = ip_to_int(addr)

    def set_sport(self, port):
        self.sport = int(port)

    def set_dport(self, port):
        self.dport = int(port)

    def read(self):
        if os.path.exists(self.path):
            print open(self.path).read()
        else:
            print "%s: not exists" % self.path

    def write(self):
        data = struct.pack("IIII",
                self.saddr, self.daddr,
                self.sport, self.dport)

        open(self.path, 'w').write(data)
        print "*********write over*********"
        self.read()


def ip_to_int(ip):
    n = socket.inet_aton(ip)
    n = struct.unpack('I', n)[0]
    print "%s -- > %s" %(ip, n)
    return n


def set_config():
    f = Filter()
    f.init(args)
    f.write()

def read_config():
    Filter().read()


class G:
    output = None
    recv = 0
    handle=[0]



def receive_signal(signum, stack):
    print 'Received: %s' % G.recv
    sys.exit(0)



signal.signal(signal.SIGINT, receive_signal)


def handle_print(data):
    print data,
    sys.stdout.flush()


def handle_write(data):
    G.output.write(data)

def read():
    f = open('/proc/net/tcpprobe')
    while True:
        d = f.readline()
        if not d:
            break
        G.recv += len(d)
        G.handle[0](d)

def main():
    set_config()
    G.handle[0] = handle_print
    if args.o:
        G.output = open(args.o, 'w')
        G.handle[0] = handle_write
    read()

main()



