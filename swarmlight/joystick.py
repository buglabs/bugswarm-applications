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
    swarm_id = "d0e0de97f0b1ebe17762654f209b3bd100de6bf6"
    resource_id = "cf8e6e43665720c74cd2923d6e2500ead12f56a7"
    produce_init(hostname, api_key, swarm_id, resource_id)

    # connect and send initialization message
    pygame.init()
    global j
    j = pygame.joystick.Joystick(0)
    j.init()
    send_message('{"message": {"to": ["d0e0de97f0b1ebe17762654f209b3bd100de6bf6"], "payload": "Joystick Initialized: %s"}}' %(j.get_name()))

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
        msg = '{"message": {"to": ["d0e0de97f0b1ebe17762654f209b3bd100de6bf6"], "payload": "Joystick Connected"}}'
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
                    button_down = e.button + 1
                    if button_down == 1:
                        send_message('{"message": {"to": ["d0e0de97f0b1ebe17762654f209b3bd100de6bf6"], "payload": "REDON"}}')
                    elif button_down == 2:
                        send_message('{"message": {"to": ["d0e0de97f0b1ebe17762654f209b3bd100de6bf6"], "payload": "YELLOWON"}}')
                    elif button_down == 3:
                        send_message('{"message": {"to": ["d0e0de97f0b1ebe17762654f209b3bd100de6bf6"], "payload": "GREENON"}}')
                    elif button_down == 5:
                        send_message('{"message": {"to": ["d0e0de97f0b1ebe17762654f209b3bd100de6bf6"], "payload": "XMASON"}}')
                    elif button_down == 6:
                        send_message('{"message": {"to": ["d0e0de97f0b1ebe17762654f209b3bd100de6bf6"], "payload": "XMASOFF"}}')
                elif event_name == 'JoyButtonUp':
                    button_up = e.button + 1
                    if button_up == 1:
                        send_message('{"message": {"to": ["d0e0de97f0b1ebe17762654f209b3bd100de6bf6"], "payload": "REDOFF"}}')
                    elif button_up == 2:
                        send_message('{"message": {"to": ["d0e0de97f0b1ebe17762654f209b3bd100de6bf6"], "payload": "YELLOWOFF"}}')
                    elif button_up == 3:
                        send_message('{"message": {"to": ["d0e0de97f0b1ebe17762654f209b3bd100de6bf6"], "payload": "GREENOFF"}}')
                elif e.type == pygame.USEREVENT:
                    send_message('{"message": {"to": ["d0e0de97f0b1ebe17762654f209b3bd100de6bf6"], "payload": "\n"}}')
    except KeyboardInterrupt:
        j.quit()
        conn.close()
                     
            
main()
