#!/usr/bin/python
import os

f = open("/home/root/swarmlight/xmaslights/xmaslights_fifo")

while(1):
    l = f.readline()
    if l.find("XMASON") > -1:
        print "ON!"
        os.system('heyu on A2')
    elif l.find("XMASOFF") > -1:
        print "OFF!"
        os.system('heyu off A2')
