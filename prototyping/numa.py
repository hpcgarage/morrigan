import sst
import sys
import os
import params2
from morriganutils import mk, mklink
from math import floor, sqrt

# The CMG class builds a single core group. It needs a group_id as input as well as
# network connections. It will build a L1 cache for each core, an L2, and a
# memory controller. All of this will be attached to the network.
# Right now, all the links have the same latency.
class CMG:
    def __init__(self, group_id, cores_per_group, net, latency):
        # Make L1-L2 bus
        bus = mk(sst.Component("L1L2Bus", "memHierarchy.Bus"), params.bus)

        # Make L1s, connect to bus
        for i in range(cores_per_group):
            sst.pushNamePrefix("Core"+str(i))

            l1 = mk(sst.Component("L1Cache", "memHierarchy.Cache"), params.l1)
            mklink((ariel, "cache_link_"+str(group_id*cores_per_group+i), latency),
                   (l1,    "high_network_0", latency)).setNoCut()
            mklink((l1,    "low_network_0", latency),
                   (bus,   "high_network_"+str(i), latency))

            sst.popNamePrefix()

        # Make L2, attach to the bus to the l1
        l2        = mk(sst.Component("L2Cache","memHierarchy.Cache"), params.l2)
        l2cpulink = mk(l2.setSubComponent("cpulink", "memHierarchy.MemLink"), params.memlink)

        mklink((bus,       "low_network_0", latency),
               (l2cpulink, "port", latency))

        # Attach L2 to network
        l2nic  = mk(l2.setSubComponent("memlink", "memHierarchy.MemNIC"), params.l2nic)
        l2link = mk(l2nic.setSubComponent("linkcontrol", "kingsley.linkcontrol"), params.linkcontrol)

        mklink((l2link, "rtr_port", latency),
               (net,    "local0",   latency))

        # Make Directory, link to network
        dc     = mk(sst.Component("Directory","memHierarchy.DirectoryController"), params.dc[group_id])
        dcnic  = mk(dc.setSubComponent("cpulink", "memHierarchy.MemNIC"), params.dcnic)
        dclink = mk(dcnic.setSubComponent("linkcontrol", "kingsley.linkcontrol"), params.linkcontrol)

        mklink((net,    "local1",   latency),
               (dclink, "rtr_port", latency))

        # Memory controller, linked to dc
        memctrl = mk(sst.Component("MemoryController","memHierarchy.MemController"), params.memctrl[group_id])
        memory  = mk(memctrl.setSubComponent("backend", "memHierarchy.dramsim3"), params.dramsim3)

        mklink((dc,      "memory",      latency),
               (memctrl, "direct_link", latency))

# Returns a list of row lengths for the grid
# Describes a grid that is as sqaure as possible
def shape(N):
    if (N < 1):
        raise ValueError("input must be positive")
    sq = floor(sqrt(N))
    ex = N - sq*sq
    rows = [sq] * sq
    for r in range(sq):
        if (ex == 0):
            break
        rows[r] += 1
        ex -= 1
    if (ex != 0):
        rows.append(ex)
    return rows

# TODO: Make all of the following configurable on the command line
# input: ncpu, ngroup, exe, args
#parser = argparse.ArgumentParser(description='Run a Fujitsu A64FX-like processor simulation')
#parser.add_argument('--ncpu',

# Check input
try:
    ncpu = int(os.environ["OMP_NUM_THREADS"])
except KeyError:
    print("Warning: OMP_NUM_THREADS not set. Defaulting to 4 threads.")
    ncpu = os.environ["OMP_NUM_THREADS"] = str(4)
    ncpu = 4

print("ncpu: " + str(ncpu))

exe = "./mml"
args = "100".split(" ")

ngroup = 4

if (ncpu % ngroup != 0):
    print("Error: ngroup does not divide ncpu")
    sys.exit(1)

cores_per_group = ncpu // ngroup

# Static Parameters TODO
default_latency = "1000ps"
# TODO -prefetchers

# Initialize our Param object
params = params2.Param(ncpu, ngroup, exe, args)

#################
## SIM WIRE UP ##
#################
ariel = mk(sst.Component("Ariel","ariel.ariel"), params.ariel)

# Create grid, connect grid
# As we do this row by row, we need only connect to
# nodes above or to the left of the current one
# And add compute to grid
grid_shape = shape(ngroup)
grid = {}
for row in range(len(grid_shape)):
    for col in range(grid_shape[row]):
        sst.pushNamePrefix("CMG{{{},{}}}".format(row,col))
        grid[(row, col)] = mk(sst.Component("Router","kingsley.noc_mesh"), params.noc)
        CMG(row*grid_shape[0]+col, cores_per_group, grid[(row, col)], default_latency)
        if (row != 0):
            mklink((grid[(row  , col)], "north", default_latency),
                   (grid[(row-1, col)], "south", default_latency))
        if (col != 0):
            mklink((grid[(row, col  )], "west", default_latency),
                   (grid[(row, col-1)], "east", default_latency))
        sst.popNamePrefix()

# Define SST core options
sst.setProgramOption("timebase", "1ps")
sst.setProgramOption("stopAtCycle", "0 ns")
sst.setStatisticLoadLevel(1)
sst.setStatisticOutput("sst.statOutputCSV", {"filepath" : "./numa_output_" + str(ncpu) + ".csv",
                                                 "separator" : ", " } )

