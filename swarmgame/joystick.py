#!/usr/bin/python

import httplib
import time
import pygame
from pygame import locals

conn = None;
j = None;

def main():
    hostname = "api.bugswarm.net"
    api_key = "a35c8276f241a967d8bdf59a07d4b5d522447b17"
    swarm_id = "74b9ae0e70eebb084d5e97014a1a29668911c070"
    resource_id = "e6af10a0d87e9c530194ae887248cbbb2ecdf83b"
    produce_init(hostname, api_key, swarm_id, resource_id)

    # connect and send initialization message
    pygame.init()
    global j
    j = pygame.joystick.Joystick(0)
    j.init()
    send_message('{"message": {"to": ["74b9ae0e70eebb084d5e97014a1a29668911c070"], "payload": "Joystick Initialized: %s"}}' %(j.get_name()))

    # send a blank message every 30 secs to maintain connection
    pygame.time.set_timer(pygame.USEREVENT, 30000)
    
    # listen for joystick events and produce their information
    listen_and_produce()

def produce_init(hostname, api_key, swarm_id, resource_id):
    # establish headers
    global conn
    conn = httplib.HTTPConnection(hostname)
    sel = '/stream?swarm_id=%s&resource_id=%s' %(swarm_id, resource_id)
    conn.putrequest('POST', sel)
    conn.putheader("x-bugswarmapikey", api_key)
    conn.putheader("transfer-encoding", "chunked")
    conn.putheader("connection", "keep-alive")
    conn.endheaders()

    # wait for the headers to return
    time.sleep(1)

    # send initial message
    try:
        msg = '{"message": {"to": ["74b9ae0e70eebb084d5e97014a1a29668911c070"], "payload": "Joystick Connected"}}'
        size = hex(len(msg))[2:] + "\r\n"
        chunk = msg + "\r\n"
        conn.send(size+chunk)

    except Exception as e:
        print 'A problem has occured: ', e            

def send_message(msg):
    # send the specified message
    try:
        size = hex(len(msg))[2:] + "\r\n"
        chunk = msg + "\r\n"
        conn.send(size+chunk)
    
    except Exception as e:
        print 'A problem has occured: ', e

def listen_and_produce():
    try:
        while True:
            for e in pygame.event.get():
                event_name = pygame.event.event_name(e.type)
                if event_name == 'JoyButtonDown':
                    send_message('{"message": {"to": ["74b9ae0e70eebb084d5e97014a1a29668911c070"], "payload": {"%i" : "DOWN"}}}' %(e.button + 1))
                elif event_name == 'JoyButtonUp':
                    send_message('{"message": {"to": ["74b9ae0e70eebb084d5e97014a1a29668911c070"], "payload": {"%i" : "UP"}}}' %(e.button + 1))
                elif event_name == 'JoyAxisMotion':
                    axis = e.axis
                    value = e.value
                    if (axis > 0 and value < 0) or (axis == 0 and value > 0 and value < .003):
                        axis = "Y"
                        value = "FORWARD"
                    elif (axis > 0 and value > 0) or (axis == 0 and value > .007 and value < 1):
                        axis = "Y"
                        value = "BACKWARD"
                    elif (axis > 0 and value == 0) or (axis == 0 and value > .003 and value < 1):
                        axis= "Y"
                        value = "STOP"
                    elif axis == 0 and value > 0:
                        axis = "X"
                        value = "FORWARD"
                    elif (axis == 0 and value == 1) or (axis == 0 and value < 0):
                        axis="X"
                        value = "BACKWARD"
                    elif axis == 0 and value == 0:
                        axis = "X"
                        value = "STOP"
                    send_message('{"message": {"to": ["74b9ae0e70eebb084d5e97014a1a29668911c070"], "payload": {"%s" : "%s"}}}' %(axis, value))
                elif e.type == pygame.USEREVENT:
                    send_message('{"message": {"to": ["74b9ae0e70eebb084d5e97014a1a29668911c070"], "payload": "\n"}}')
    except KeyboardInterrupt:
        j.quit()
        conn.close()
                     
            
main()
