#!/bin/bash
mkfifo slfifo &&
./swarmlight.py &
./bugswarm-tools/consume.py consume 3f661d513bda60bd41419666dd8fa381ec17e979 > slfifo &