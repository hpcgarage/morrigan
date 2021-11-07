import sst
import sys
import params
import morriganutils as mu

# Define SST core options
sst.setProgramOption("timebase", "1ps")
sst.setProgramOption("stopAtCycle", "0 ns")

# CPU and generator
comp_cpu = mu.mk(sst.Component("cpu", "miranda.BaseCPU"), params.miranda_cpu)
gen      = mu.mk(comp_cpu.setSubComponent("generator", "miranda.Stencil3DBenchGenerator"), params.miranda_3dgen)

# 2 Levels of cache
comp_l1cache = mu.mk(sst.Component("l1cache", "memHierarchy.Cache"), params.l1)
comp_l2cache = mu.mk(sst.Component("l2cache", "memHierarchy.Cache"), params.l2)

# Memory controller
memctrl = mu.mk(sst.Component("memory", "memHierarchy.MemController"), params.memctrl)
memory  = mu.mk(memctrl.setSubComponent("backend", "memHierarchy.simpleMem"), params.simplemem)

# Define the simulation links
link = mu.mklink((comp_cpu, "cache_link", "1000ps"), (comp_l1cache, "high_network_0", "1000ps"))
link.setNoCut()
mu.mklink((comp_l1cache, "low_network_0", "1000ps"), (comp_l2cache, "high_network_0", "1000ps"))
mu.mklink((comp_l2cache, "low_network_0", "50ps"), (memctrl, "direct_link", "50ps"))
