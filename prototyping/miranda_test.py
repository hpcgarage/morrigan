import sst
import sys
import os
import params2
import argparse
from morriganutils import mk, mklink
from math import floor, sqrt

# Parse arguments
parser = argparse.ArgumentParser(description='Run a Fujitsu A64FX-like processor simulation',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-w', '--workload', default='ariel', help='Which workload to run', type=str)
config = parser.parse_args(sys.argv[1:])

# Display configuration
print('Running with configuration: {}'.format(vars(config)))

# Static Parameters TODO - fix these up
default_latency = "1000ps"
# TODO -prefetchers

freq             = "2.0GHz"
cache_line_bytes = "64"
coherence        = "MESI"
replacement      = "lru"

# Params
params_ariel   = {
    "verbose"        : 0,
    "corecount"      : 1,
    "cachelinesize"  : cache_line_bytes,
    "executable"     : './mmb',
    "appargcount"    : 2,
    "apparg0"        : 100,
    "apparg1"        : 10,
    "clock"          : freq,
    "arielmode"      : 0,
}

params_l1 = {
    "cache_frequency"       : freq,
    "cache_size"            : "4KiB",
    "associativity"         : "4",
    "access_latency_cycles" : "2",
    "L1"                    : "1",
    "cache_line_size"       : cache_line_bytes,
    "coherence_protocol"    : coherence,
    "replacement_policy"    : replacement,
    "debug"                 : "0",
}

params_l2 = {
    "access_latency_cycles" : "20",
    "cache_frequency"       : freq,
    "replacement_policy"    : replacement,
    "coherence_protocol"    : coherence,
    "associativity"         : "4",
    "cache_line_size"       : cache_line_bytes,
    "prefetcher"            : "cassini.StridePrefetcher",
    "debug"                 : "0",
    "L1"                    : "0",
    "cache_size"            : "1MiB",
    "mshr_latency_cycles"   : "5",
}

params_dramsim3 = {
    "config_ini"  : "../DRAMsim3/configs/DDR3_1Gb_x8_1333.ini",
    "mem_size"    : "1GiB",
}

params_mc = {
    "addr_range_start" : 0,
    "addr_range_end"   : 1024*1024*1024-1,
    "clock"   : freq,
    "backing" : "none",
}

params_miranda = {
    "clock" : freq,
}

params_gen = {
    "dim" : 16,
    "block" : 2,
    "size" : 8,
}

#################
## SIM WIRE UP ##
#################

# L1
l1 = mk(sst.Component("L1Cache", "memHierarchy.Cache"), params_l1)

# L2
l2 = mk(sst.Component("L2Cache","memHierarchy.Cache"), params_l2)

# MC
mc = mk(sst.Component("MemoryController","memHierarchy.MemController"), params_mc)

# Mem
mem = mk(mc.setSubComponent("backend", "memHierarchy.dramsim3"), params_dramsim3)

# Ariel / Miranda
if (config.workload == 'ariel'):
    ariel = mk(sst.Component("Ariel","ariel.ariel"), params_ariel)
    cpuport = (ariel, "cache_link_0", default_latency)
elif (config.workload == 'miranda'):
    miranda = mk(sst.Component("Miranda", "miranda.BaseCPU"), params_miranda)
    gen     = mk(miranda.setSubComponent("generator", "miranda.MMGenerator"), params_gen)
    cpuport = (miranda, "cache_link", default_latency)
else:
    print("UNKNOWN WORKLOAD")
    sys.exit(1)


mklink(cpuport,
       (l1, "high_network_0", default_latency))

mklink((l1, "low_network_0", default_latency),
       (l2, "high_network_0", default_latency))

mklink((l2, "low_network_0", default_latency),
       (mc, "direct_link", default_latency))

# Define SST core options
sst.setProgramOption("timebase", "1ps")
#sst.setProgramOption("stopAtCycle", "0 ns")
#sst.setStatisticLoadLevel(9)
#sst.enableAllStatisticsForAllComponents()
outfile = "./miranda_test_output_" + config.workload + ".csv"
print("Writng to " + outfile)
sst.setStatisticOutput("sst.statOutputCSV", {"filepath" : outfile, "separator" : ", " } )

