# Morrígan Project

The Morrígan project is aimed at adding phase detection and model swapping capabilities to the [Structural Simulation Toolkit](https://sst-simulator.org/). 

## All Steps

```
git clone git@github.com:hpcgarage/morrigan.git
cd morrigan
git submodule update --init --recursive
./install-dependencies.sh
./configure-morrigan.sh # TODO: make sure this script pulls in the env for dependencies
./install-morrigan.sh # TODO: make sure this script pulls in the end for dependencies
source morrigan-env.sh
```

## Making Changes
After making changes to any of the submodules, re-run the `./install-morrigan.sh` script. You should not need to run `source` command again. 


## Testing
SST-Elements comes with an extensive suite of tests, most of which we don't need for this project. Follow these steps to test your installation of this project and the relevant dependencies.

```
... todo ...
```

## Making Changes
After making changes to any of the subprojects, re-run the `./install-morrigan.sh` script. You should not need to run `source` command again. 

## Workflow 
As mentioned above, this project relies on custom version of some other projects. If you want to make changes to those projects, you don't need to download them separately -- you can do that right from within this repo. Follow these steps to create changes and push them to our repos.

```
... todo ...
```

## Related Work

1. TODO Cite Online Model Swapping paper
2. TODO Cite reference on phase detection
