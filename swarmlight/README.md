# SwarmLight

Turn lights on and off using this application built over BUGswarm.

## Installation

* Ensure that [heyu](http://www.heyu.org/) is running on the BUG.
* Fork this repository and from the root directory:

```shell
git submodule init
git submodule update
```

* SCP the swarmlight directory of the fork in the home directory of the BUG.
* Ensure that your external appliances (xmas lights or traffic light) are connected to the bug

## Usage

From the home directory of the BUG:

```shell
cd swarmlight/DEVICE # xmaslights/trafficlight
./DEVICE.sh
```

Visit the [SwarmLight](http://developer.bugswarm.net/swarmlight.html) website to turn the lights on and off.