import sst
import os

groups          = 4   # Number of CMGs (core memory groups)
cores_per_group = 12  # Compute cores per CMG

clock         = "2GHz"   # Core clock
memory_clock  = "200MHz" #TODO

coherence_protocol = "MESI"

l1_prefetch_params = {}
l2_prefetch_params = {}

# [mm.12] Each L1I is 64KiB, 4-way associative
l1_params = {
    "coherence_protocol"   : coherence_protocol,
    "cache_frequency"      : clock,
    "replacement_policy"   : "lru",   # assumed based on [mm.78]
    "cache_size"           : "64KiB",
    "maxRequestDelay"      : "10000", # Note - originally was 1000000ns
    "associativity"        : 4,
    "cache_line_size"      : 256,
    "access_latency_cycles": 5,       # [mm.64] - 5 is minimum, longer for sve
    "L1"                   : 1,
    "debug"                : 0
}

# [mm.12] Each L2 (one per CMG) is 8MiB, 16-way associative
l2_params = {
    "coherence_protocol"   : coherence_protocol,
    "cache_frequency"      : clock,
    "replacement_policy"   : "lru",  # assumed LRU - see l1_params
    "cache_size"           : "8MiB",
    "associativity"        : 16,
    "cache_line_size"      : 256,
    "access_latency_cycles": 37,     # [mm.65] - 37 minimum, 47 max
    "mshr_num_entries"     : 256,    # [mm.66] - size of MIB
    "mshr_latency_cycles"  : 2,      # Note - unspecified, leaving as is
    "debug": 0,
    # Prefetch params
    "prefetcher"           : "cassini.StridePrefetcher",
    "reach"                : 16,
    "detect_range"         : 1
}

ariel_params = { #TODO
    "verbose"             : "0",
    "maxcorequeue"        : "256",
    "maxtranscore"        : "16",
    "maxissuepercycle"    : "2",
    "pipetimeout"         : "0",
    "executable"          : str('/home/plavin3/morrigan/example/stream'),
    "appargcount"         : "0",
    "arielinterceptcalls" : "1",
    "launchparamcount"    : 1,
    "launchparam0"        : "-ifeellucky",
    "arielmode"           : "1",
    "corecount"           : groups * cores_per_group,
    "clock"               : str(clock)
}

ariel_memmgr_params = { # TODO
    "memmgr.pagecount0"   : "1048576",
}

# Create Ariel component
ariel = sst.Component("A0", "ariel.ariel")
ariel.addParams(ariel_params)

# Use a first-touch memory manager
memmgr = ariel.setSubComponent("memmgr", "ariel.MemoryManagerSimple")
memmgr.addParams(ariel_memmgr_params)

# Create an L1D for each core

for group in range(groups):
    
    for core_id in range(cores_per_group):

        l1 = sst.Component("l1cache_" + str(core_id), "memHierarchy.Cache")
        l1.addParams(l1_params)
