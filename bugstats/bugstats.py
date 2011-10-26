#!/usr/bin/python

import httplib
import time
import subprocess
import threading
import sys
import json
from datetime import datetime

conn = None
hostname = "api.bugswarm.net"
api_key = "a35c8276f241a967d8bdf59a07d4b5d522447b17"
swarm_id = "83537f005a15bc5f65935997ef858461c8f86608"
resource_id = "7ebaf88e69998588f961c2aaf9950e8f1409371a"

def main():
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
    try:
        interval_producer = IntervalProducer()
        immediate_producer = ImmediateProducer()
        interval_producer.start()
        immediate_producer.start()
        
    except KeyboardInterrupt:
        global conn
        conn.close()
        interval_producer._running = False
        immediate_producer._running = False

def send_message(msg):
    try:
        size = hex(len(msg))[2:] + "\r\n"
        chunk = msg + "\r\n"
        conn.send(size+chunk)
    
    except Exception as e:
        print 'A problem has occured: ', e

def produce_stats_public():
    stats = get_stats()
    message = '{"message": {"to": ["%s"], "payload": %s}}'%(swarm_id, stats)
    send_message(message)

def get_stats():
    global swarm_id
    stats = {}
    mpstat_out = [x for x in subprocess.Popen("mpstat", stdout=subprocess.PIPE).stdout.readlines()[-1].strip().split(" ") if len(x) != 0]
    stats["usr"] = mpstat_out[3]
    stats["nice"] = mpstat_out[4]
    stats["sys"] = mpstat_out[5]
    stats["datetime"] = str(datetime.now())
    return json.dumps(stats)

class IntervalProducer(threading.Thread):

    _running = True

    def run(self):
        t = threading.Timer(5, self.interval_stats)
        t.start()

    def interval_stats(self):
        produce_stats_public()
        if self._running:
            t = threading.Timer(5, self.interval_stats)
            t.start()

class ImmediateProducer(threading.Thread):

    _running = True

    def run(self):
        self.consume_and_respond()

    def consume_and_respond(self):
        global conn
        resp = conn.getresponse()
        
        stanza = ""
        while self._running:
            stanza += resp.read(1)
            if stanza.endswith("\r\n"):
                stanza_json = json.loads(stanza)
                for key in stanza_json:
                    if key == 'message':
                        message_content = stanza_json['message']
                        if message_content['payload'] == 'stats':
                            produce_stats_public()
                            
                print stanza
                stanza = ""

main()

