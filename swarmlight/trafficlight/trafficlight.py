#!/usr/bin/python
import socket

HOST = '192.168.0.176'
PORT = 23
f = open("/home/root/swarmlight/trafficlight/trafficlight_fifo")

while(1):
    l = f.readline()
    if l.find("REDON") > -1:
        print "RED ON!"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send("RED ON\r\n")
        data = s.recv(1024)
        s.close()
    elif l.find("REDOFF") > -1:
        print "RED OFF!"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send("RED OFF\r\n")
        data = s.recv(1024)
        s.close()
    elif l.find("GREENON") > -1:
        print "GREEN ON!"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send("GREEN ON\r\n")
        data = s.recv(1024)
        s.close()
    elif l.find("GREENOFF") > -1:
        print "GREEN OFF!"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send("GREEN OFF\r\n")
        data = s.recv(1024)
        s.close()
    elif l.find("YELLOWON") > -1:
        print "YELLOW ON!"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send("YELLOW ON\r\n")
        data = s.recv(1024)
        s.close()
    elif l.find("YELLOWOFF") > -1:
        print "YELLOW OFF!"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send("YELLOW OFF\r\n")
        data = s.recv(1024)
        s.close()
