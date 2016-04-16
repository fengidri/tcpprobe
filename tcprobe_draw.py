# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2016-04-13 05:10:16
#    email     :   fengidri@yeah.net
#    version   :   1.0.1




def parser_tcpprobe(f):
    infos = {}

    lines = open(f).readlines()
    for line in lines:
        t = line.split()
        if line[0] == '#':
            continue

        con = "%s->%s" % (t[1], t[2])
        if infos.get(con):
            info = infos.get(con)
        else:
            info = {'ssthresh':[],
                    'cwnd':[],
                    'timestamp':[]}
            infos[con] = info

        info = infos.get(con)

        info['cwnd'].append(float(t[6]))
        info['ssthresh'].append(float(t[7]))
        info['timestamp'].append(float(t[0]))
    return infos



import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter
import sys

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="tcpprobe log", default = None, required= True)
parser.add_argument("-o", help="output file", default = None, required= True)
parser.add_argument("-s", help= "select con by index", default = None, type=int)


args = parser.parse_args()


infos = parser_tcpprobe(args.i)
cons = infos.keys()
cons.sort()
if len(infos) > 1 and not args.s:
    i = 0
    for con in cons:
        print "%s: %s" % (i, con)
        i += 1
    sys.exit(0)


print "draw conn: %s" % cons[args.s]

info = infos[cons[args.s]]


plt.plot(info['timestamp'], info['cwnd'],  label = 'cwnd')
plt.plot(info['timestamp'], info['ssthresh'], label = 'ssthresh')
plt.legend()
plt.title('tcpprobe')
plt.xlabel('time/s')
plt.ylabel('cwnd/ssthresh')
plt.savefig(args.o)

