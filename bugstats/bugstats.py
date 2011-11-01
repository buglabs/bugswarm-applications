#!/usr/bin/python

import httplib
import time
import subprocess
import threading
import sys
import json
import signal
import socket
import random
from datetime import datetime
from optparse import OptionParser

conn = None
hostname = "api.bugswarm.net"
api_key = "7a849e6548dbd6f8034bb7cc1a37caa0b1a2654b"
swarm_id = "0c966d48e16908975ae483642ed7302e7b6ec7d7"
resource_map = {"1":"1c85f72ef0a57fc2722540294e349343fccfd1c1", "2":"1f8757afbd3b814f85e1da02fe6ce1c802abb1a7", "3":"6a7166dd0f14cdca9b95f260cbee86129aac8991", "4":"29f7ba8c5fc61cbf3fc97f43d72b755c55073cfd", "5":"9cd5ee810ca0f8ed99114ef5e17afa854e3852ea", "6":"8969c03718274cbb62be0ab056b9d37c6471fe4a", "7":"b1eb3f1c13b581a1f5b962e4d5378f10f06780dd", "8":"39525163ebef8bc83dc6fd891e7cea1e8fe21987", "9":"a540cd12f6e098cdde71404bab964a2302da2f23", "10":"4588344415bc95e0edd00a51e33452ab70808878"}
resource_id = None
latitude = None
longitude = None
produce_fake = False
interval_producer = None
immediate_producer = None

def main():
    opt_usage = "usage: \n %s BUG_NUMBER [options]"%(sys.argv[0])
    opt_usage += "\n\n *BUG_NUMBER: The number of the BUG you are running BUGstats for. Valid numbers; 1-10."
    parser = OptionParser(usage = opt_usage)
    parser.add_option("-f", action="store_true", dest="fake", help="Run with fake statistics.", default=False)
    (options, args) = parser.parse_args()
    if len(args) != 1:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    bug_number = args[0]
    bugstats(bug_number, options.fake)

def bugstats(bug_number, fake):
    global resource_id, produce_fake, latitude, longitude
    try:
        if (int(bug_number) > 10) or (int(bug_number < 1)):
            print "BUG_NUMBER must be between 1 and 10"
            sys.exit()
    except ValueError:
        print "BUG_NUMBER must be an integer between 1 and 10"
        sys.exit()
    resource_id = get_resource_id(bug_number)
    if fake == True:
        produce_fake = True
    latitude = round(random.uniform(39.7, 40.2), 2)
    longitude = round(random.uniform(-73.5, -74.5), 2)
    signal.signal(signal.SIGINT, signal_handler)
    swarm_init()
    participate()

def get_resource_id(bug_number):
    return resource_map[bug_number]

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
    global produce_fake
    if produce_fake == True:
        stats = get_fake_stats()
    else:
        stats = get_stats()
    if isImmediate == True:
        stats["immediate"] = True;
    else:
        stats["immediate"] = False;
    statsJSON = json.dumps(stats);
    message = '{"message": {"to": ["%s"], "payload": %s}}'%(swarm_id, statsJSON)
    send_message(message)

def get_stats():
    global latitude, longitude
    stats = {}
    mpstat_out = [x for x in subprocess.Popen("mpstat", stdout=subprocess.PIPE).stdout.readlines()[-1].strip().split(" ") if len(x) != 0]
    stats["usr"] = mpstat_out[3]
    stats["nice"] = mpstat_out[4]
    stats["sys"] = mpstat_out[5]
    stats["datetime"] = str(datetime.now())
    stats["position"] = {"lat": latitude, "lon": longitude}
    return stats

def get_fake_stats():
    global latitude, longitude
    stats = {}
    stats["usr"] = random.uniform(0,10)
    stats["nice"] = random.uniform(0,10)
    stats["sys"] = random.uniform(0,10)
    stats["datetime"] = str(datetime.now())
    stats["position"] = {"lat": latitude, "lon": longitude}
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

