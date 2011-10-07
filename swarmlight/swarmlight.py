#!/usr/bin/python
import os

f = open("/home/root/swarmlight/slfifo")

while(1):
    l = f.readline()
    if l.find("LIGHTON") > -1:
        print "ON!"
        os.system('heyu on A2')
    elif l.find("LIGHTOFF") > -1:
        print "OFF!"
        os.system('heyu off A2')
