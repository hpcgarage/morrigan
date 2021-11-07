import sst
import sys
import params
from morriganutils import mk, mklink, anon

ncpu = 6

# Define SST core options
sst.setProgramOption("timebase", "1ps")
sst.setProgramOption("stopAtCycle", "0 ns")

# L1-L2 Bus
bus = mk(sst.Component("bus", "memHierarchy.Bus"), {"bus_frequency" : "2.0GHz"})

for i in range(ncpu):
    cpu  = mk(anon("miranda.BaseCPU"), params.miranda_cpu)
    gen  = mk(cpu.setSubComponent("generator", "miranda.Stencil3DBenchGenerator"), params.miranda_3dgen)
    l1   = mk(anon("memHierarchy.Cache"), params.l1)
    mklink((cpu, "cache_link", "1000ps"),(l1, "high_network_0", "1000ps")).setNoCut()
    mklink((l1, "low_network_0", "1000ps"), (bus, "high_network_" + str(i), "1000ps"))

#L2 Cache
l2cache = mk(sst.Component("l2cache", "memHierarchy.Cache"), params.l2)

# Memory controller
memctrl = mk(sst.Component("memory", "memHierarchy.MemController"), params.memctrl)
memory  = mk(memctrl.setSubComponent("backend", "memHierarchy.simpleMem"), params.simplemem)

# Define the simulation links
mklink((bus, "low_network_0", "1000ps"), (l2cache, "high_network_0", "1000ps"))
mklink((l2cache, "low_network_0", "50ps"), (memctrl, "direct_link", "50ps"))
