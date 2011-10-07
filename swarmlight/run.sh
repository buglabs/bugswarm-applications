#!/bin/bash
mkfifo slfifo &&
sleep 1
./swarmlight.py &
sleep 1
nohup ./bugswarm-tools/consume.py consume 3f661d513bda60bd41419666dd8fa381ec17e979 > slfifo &