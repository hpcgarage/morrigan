import sst
import sys
import os
import params
from morriganutils import mk, mklink, anon

try:
    ncpu = int(os.environ["OMP_NUM_THREADS"])
except KeyError:
    print("Error: OMP_NUM_THREADS not set. Aborting.")
    sys.exit(1)

print("ncpu: " + str(ncpu))

exe = "./rand"
args = "1000".split(" ")

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

for i in range(len(args)):
    ariel_params["apparg" + str(i)] = args[i]

# Define SST core options
sst.setProgramOption("timebase", "1ps")
sst.setProgramOption("stopAtCycle", "0 ns")

# Set up ariel
ariel = mk(anon("ariel.ariel"), ariel_params)

# L1-L2 Bus
bus = mk(sst.Component("bus", "memHierarchy.Bus"), {"bus_frequency" : "2.0GHz"})

for i in range(ncpu):
    l1   = mk(anon("memHierarchy.Cache"), params.l1)
    l1.enableStatistics("TotalEventsReceived")
    mklink((ariel, "cache_link_"+str(i), "1000ps"),(l1, "high_network_0", "1000ps")).setNoCut()
    mklink((l1, "low_network_0", "1000ps"), (bus, "high_network_" + str(i), "1000ps"))

#L2 Cache
l2cache = mk(sst.Component("l2cache", "memHierarchy.Cache"), params.l2)

#L3 Cache
l3cache = mk(sst.Component("l3cache", "memHierarchy.Cache"), params.l3)

#DRAMsim3

# Memory controller
memctrl = mk(sst.Component("memory", "memHierarchy.MemController"), params.memctrl)
memory  = mk(memctrl.setSubComponent("backend", "memHierarchy.dramsim3"), params.dramsim3)

# Define the simulation links
mklink((bus, "low_network_0", "1000ps"), (l2cache, "high_network_0", "1000ps"))
mklink((l2cache, "low_network_0", "50ps"), (l3cache, "high_network_0", "50ps"))
mklink((l3cache, "low_network_0", "50ps"), (memctrl, "direct_link", "50ps"))

sst.setStatisticLoadLevel(1)
sst.setStatisticOutput("sst.statOutputCSV", {"filepath" : "./ariel_rand_output_" + str(ncpu) + ".csv",
                                             "separator" : ", " } )

