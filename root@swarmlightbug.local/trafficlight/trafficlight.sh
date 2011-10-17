#!/bin/bash
mkfifo trafficlight_fifo &&
sleep 1
./trafficlight.py &
sleep 1
nohup ../bugswarm-tools/consume.py consume d0e0de97f0b1ebe17762654f209b3bd100de6bf6 e506babbe42b3ca5f589697e06ba74003d9a8009 > trafficlight_fifo &