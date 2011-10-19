#!/bin/bash
mkfifo xmaslights_fifo &&
sleep 1
./xmaslights.py &
sleep 1
nohup ../bugswarm-tools/consume.py consume d0e0de97f0b1ebe17762654f209b3bd100de6bf6 9d123ba8322342e9e28edefd6c94fdcf2d1aa45a > xmaslights_fifo &