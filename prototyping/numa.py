import sst
import sys
import os
import params2
from morriganutils import mk, mklink, anon
from math import floor, sqrt

try:
    ncpu = int(os.environ["OMP_NUM_THREADS"])
except KeyError:
    print("Warning: OMP_NUM_THREADS not set. Defaulting to 4 threads.")
    ncpu = 4
    #print("Error: OMP_NUM_THREADS not set. Aborting.")
    #sys.exit(1)

print("ncpu: " + str(ncpu))

exe = "./mml"
args = "100".split(" ")

ariel_params = {
    "verbose"        : 0,
    "corecount"      : ncpu,
    "cachelinesize"  : 256,
    "executable"     : exe,
    "appargcount"    : len(args),
    "envparamcount"  : 1,
    "envparamname0"  : "OMP_NUM_THREADS",
    "envparamval0"   : str(ncpu),
    "clock"          : "2.0GHz",
    "arielmode"      : 0,
}

ngroup = 1

if (ncpu % ngroup != 0):
    print("Error: ngroup does not divide ncpu")
    sys.exit(1)

cores_per_group = ncpu // ngroup

for i in range(len(args)):
    ariel_params["apparg" + str(i)] = args[i]


# Set up ariel
ariel = mk(anon("ariel.ariel"), ariel_params)

default = "1000ps"
# TODO -prefetchers

bus_params = {
    "bus_frequency" : "2.0GHz",
}


class CMG:
    def __init__(self, group_id, net):
        # Make L1-L2 bus
        bus = mk(anon("memHierarchy.Bus"), params.bus)

        # Make L1s, connect to bus
        for i in range(cores_per_group):
            l1 = mk(anon("memHierarchy.Cache"), params.l1)
            mklink((ariel, "cache_link_"+str(group_id*cores_per_group+i), default),
                   (l1,    "high_network_0", default)).setNoCut()
            mklink((l1,    "low_network_0", default),
                   (bus,   "high_network_"+str(i), default))

        # Make L2, attach to the bus to the l1
        l2        = mk(anon("memHierarchy.Cache"), params.l2)
        l2cpulink = mk(l2.setSubComponent("cpulink", "memHierarchy.MemLink"), params.memlink)
        mklink((bus,       "low_network_0", default),
               (l2cpulink, "port", default))

        # Attach L2 to network
        l2nic  = mk(l2.setSubComponent("memlink", "memHierarchy.MemNIC"), params.l2nic)
        l2link = mk(l2nic.setSubComponent("linkcontrol", "kingsley.linkcontrol"), params.linkcontrol)
        mklink((l2link, "rtr_port", default),
               (net,    "local0",   default))

        # Make Directory, link to network
        dc     = mk(anon("memHierarchy.DirectoryController"), params.dc[group_id])
        dcnic  = mk(dc.setSubComponent("cpulink", "memHierarchy.MemNIC"), params.dcnic)
        dclink = mk(dcnic.setSubComponent("linkcontrol", "kingsley.linkcontrol"), params.linkcontrol)

        #dc = sst.Component("dc"+str(group_id), "memHierarchy.DirectoryController")
        #dcnic = dc.setSubComponent("cpulink", "memHierarchy.MemNIC")
        #dclink = dcnic.setSubComponent("linkcontrol", "kingsley.linkcontrol")

        #dc.addParams(params.dc[group_id])
        #dcnic.addParams(params.dcnic)
        #dclink.addParams(params.linkcontrol)
        #dclink.addParams({"network_link_control" : "kingsley.linkcontrol"})

        mklink((net,    "local1",   default),
               (dclink, "rtr_port", default))

        # Memory controller, linked to dc
        memctrl = mk(anon("memHierarchy.MemController"), params.memctrl[group_id])
        memory  = mk(memctrl.setSubComponent("backend", "memHierarchy.dramsim3"), params.dramsim3)
        mklink((dc,      "memory",      default),
               (memctrl, "direct_link", default))


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

# Create grid, connect grid
# As we do this row by row, we need only connect to
# nodes above or to the left of the current one
# And add compute to grid
params = params2.Param(ngroup)
grid_shape = shape(ngroup)
grid = {}
for row in range(len(grid_shape)):
    for col in range(grid_shape[row]):
        print("Creating noc ({},{})".format(row, col))
        grid[(row, col)] = mk(anon("kingsley.noc_mesh"), params.noc)
        CMG(row*grid_shape[0]+col, grid[(row, col)])
        if (row != 0):
            mklink((grid[(row  , col)], "north", default),
                   (grid[(row-1, col)], "south", default))
        if (col != 0):
            mklink((grid[(row, col  )], "west", default),
                   (grid[(row, col-1)], "east", default))

# Define SST core options
sst.setProgramOption("timebase", "1ps")
sst.setProgramOption("stopAtCycle", "0 ns")
sst.setStatisticLoadLevel(1)
sst.setStatisticOutput("sst.statOutputCSV", {"filepath" : "./numa_output_" + str(ncpu) + ".csv",
                                                 "separator" : ", " } )

