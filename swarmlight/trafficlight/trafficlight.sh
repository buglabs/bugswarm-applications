#!/bin/bash
mkfifo trafficlight_fifo &&
sleep 1
./trafficlight.py &
sleep 1
nohup ../bugswarm-tools/consume.py consume d0e0de97f0b1ebe17762654f209b3bd100de6bf6 9770a0351dd4cef12514dfdec78c9cf689dea0ca > trafficlight_fifo &