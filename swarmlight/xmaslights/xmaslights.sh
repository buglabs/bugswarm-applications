#!/bin/bash
mkfifo xmaslights_fifo &&
sleep 1
./xmaslights.py &
sleep 1
nohup ../bugswarm-tools/consume.py consume d0e0de97f0b1ebe17762654f209b3bd100de6bf6 dca15e32f0f32e070551b34f9df46e8ff9b3bd2a > xmaslights_fifo &