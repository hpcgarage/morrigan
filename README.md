# Morrígan Project

The Morrígan project is aimed at adding phase detection and model swapping capabilities to the [Structural Simulation Toolkit](https://sst-simulator.org/). 

## Step 1: Dependencies
This project automatically pulls in git submodules, and those submodules have dependencies that must be pulled in manually. For simplicity, we include a script that will install Autotools, Cmake, and Intel's Pintool in a subdirectory of this one so that they don't interfere with the rest of your system. You can skip this step if you don't need them, but if you experience issues during Step 2: Instllation, you may want to try using the versions installed by this script.

```
./install-dependencies.sh
source morrigan-env.sh
```

## Step 2: Installation
This project relies on custom versions of SST-Core, SST-Elements, and DRAMsim3. The following instructions will install the project in the directory it is downloaded in, i.e. it will not interfere with other SST installations on your machine.
```
git clone git@github.com:hpcgarage/morrigan.git
cd morrigan
git submodule update --init --recursive
./install-morrigan.sh
source morrigan-env.sh
```

## Testing
SST-Elements comes with an extensive suite of tests, most of which we don't need for this project. Follow these steps to test your installation of this project and the relevant dependencies.

```
... todo ...
```

## Workflow 
As mentioned above, this project relies on custom version of some other projects. If you want to make changes to those projects, you don't need to download them separately -- you can do that right from within this repo. Follow these steps to create changes and push them to our repos.

```
... todo ...
```

## Related Work

1. TODO Cite Online Model Swapping paper
2. TODO Cite reference on phase detection
