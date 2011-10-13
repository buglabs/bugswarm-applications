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
* Plug lights into 'X-10 Powerhouse' outlet.
* Plug the 'X-10 Powerhouse' outlet into the 'X-10 ActiveHome' outlet.
* Connect the 'X-10 ActiveHome' outlet to the BUG through a serial -> USB connection.

## Usage

From the home directory of the BUG:

```shell
cd swarmlight
./run.sh
```

Visit the [SwarmLight](http://developer.bugswarm.net/swarmlight.html) website to turn the lights on and off.