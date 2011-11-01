#!/usr/bin/python

import httplib
import time
import subprocess
import threading
import sys
import json
from datetime import datetime
import signal
import socket
import random

conn = None
hostname = "api.bugswarm.net"
api_key = "7a849e6548dbd6f8034bb7cc1a37caa0b1a2654b"
swarm_id = "0c966d48e16908975ae483642ed7302e7b6ec7d7"
resource_id = "4588344415bc95e0edd00a51e33452ab70808878"
interval_producer = None
immediate_producer = None

def main():
    signal.signal(signal.SIGINT, signal_handler)
    swarm_init()
    participate()

def swarm_init():
    global hostname, api_key, swarm_id, resource_id
    global conn
    conn = httplib.HTTPConnection(hostname)
    sel = '/stream?swarm_id=%s&resource_id=%s' %(swarm_id, resource_id)
    conn.putrequest('POST', sel)
    conn.putheader("x-bugswarmapikey", api_key)
    conn.putheader("transfer-encoding", "chunked")
    conn.putheader("connection", "keep-alive")
    conn.endheaders()
    time.sleep(1)

    try:
        msg = '{"message": {"to": ["' + swarm_id + '"], "payload": "BUG Connected"}}'
        size = hex(len(msg))[2:] + "\r\n"
        chunk = msg + "\r\n"
        conn.send(size+chunk)

    except Exception as e:
        print 'A problem has occured: ' + str(e)            

def participate():    
    global interval_producer, immediate_producer
    interval_producer = IntervalProducer()
    immediate_producer = ImmediateProducer()
    interval_producer.start()
    immediate_producer.start()
            
def send_message(msg):
    try:
        size = hex(len(msg))[2:] + "\r\n"
        chunk = msg + "\r\n"
        conn.send(size+chunk)
    
    except Exception as e:
        print 'A problem has occured: ', e

def produce_stats_public(isImmediate):
    #stats = get_stats()
    stats = get_fake_stats()
    if isImmediate == True:
        stats["immediate"] = True;
    else:
        stats["immediate"] = False;
    statsJSON = json.dumps(stats);
    message = '{"message": {"to": ["%s"], "payload": %s}}'%(swarm_id, statsJSON)
    send_message(message)

def get_stats():
    stats = {}
    mpstat_out = [x for x in subprocess.Popen("mpstat", stdout=subprocess.PIPE).stdout.readlines()[-1].strip().split(" ") if len(x) != 0]
    stats["usr"] = mpstat_out[3]
    stats["nice"] = mpstat_out[4]
    stats["sys"] = mpstat_out[5]
    stats["datetime"] = str(datetime.now())
    stats["position"] = {"lat": 40.88, "lon": -74.32}
    return stats

def get_fake_stats():
    stats = {}
    stats["usr"] = random.uniform(0,10)
    stats["nice"] = random.uniform(0,10)
    stats["sys"] = random.uniform(0,10)
    stats["datetime"] = str(datetime.now())
    stats["position"] = {"lat": 40.88, "lon": -74.32}
    return stats

def signal_handler(signal, frame):
        global conn, inverval_producer, immediate_producer
        interval_producer._running = False
        immediate_producer._running = False
        conn.send("0\r\n\r\n")
        immediate_producer.close()
        conn.close()
        print 'Http connection closed.'
        sys.exit(0)

class IntervalProducer(threading.Thread):

    _running = True

    def run(self):
        t = threading.Timer(5, self.interval_stats)
        t.start()

    def interval_stats(self):
        produce_stats_public(False)
        if self._running:
            t = threading.Timer(5, self.interval_stats)
            t.start()

class ImmediateProducer(threading.Thread):

    _running = True
    resp = None

    def run(self):
        self.consume_and_respond()

    def consume_and_respond(self):
        global conn
        self.resp = conn.getresponse()
        
        stanza = ""
        while self._running:
            stanza += self.resp.read(1)
            if stanza.endswith("\r\n"):
                stanza_json = json.loads(stanza)
                for key in stanza_json:
                    if key == 'message':
                        message_content = stanza_json['message']
                        if message_content['payload'] == 'stats':
                            produce_stats_public(True)
                            
                print stanza
                stanza = ""

    def close(self):
        print "Entered close"
        fn = self.resp.fileno()
        s = socket.fromfd(fn, socket.AF_INET, socket.SOCK_STREAM)
        s.close()
        print "Exit close"

main()

