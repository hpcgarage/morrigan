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

bus_params = {
    "bus_frequency" : clock,
}

mc_params = {
    "backing" : "none",       # we don't need to store the actual values
    "clock"   : memory_clock,
}

dramsim3_params = {
    "config_ini" : "../../DRAMsim3/configs/HBM2_8Gb_x128.in",
    "mem_size"   : "8GiB"
}

#TODO
dc_params = {
    "coherence_protocol": coherence_protocol,
    "memNIC.network_bw": memory_network_bandwidth,
    "memNIC.interleave_size": str(mem_interleave_size) + "B",
    "memNIC.interleave_step": str((groups * memory_controllers_per_group) * mem_interleave_size) + "B",
    "entry_cache_size": 256*1024*1024, #Entry cache size of mem/blocksize
    "clock": memory_clock,
    "debug": 1,
}



# Create Ariel component
ariel = sst.Component("A0", "ariel.ariel")
ariel.addParams(ariel_params)

# Use a first-touch memory manager
memmgr = ariel.setSubComponent("memmgr", "ariel.MemoryManagerSimple")
memmgr.addParams(ariel_memmgr_params)

# Functions to get the handles of the various created objects
def l1name(core, group):
    return "l1cache_c" + str(core_id) + "_g" + str(group)

def l2name(group):
    return "l2cache_g" + str(group)

def busname(group):
    return "l1l2bus_g" + str(group)

def linkname(e1, e2):
    return "link_" + e1 + "_" + e2

l1_l2_latency = "1000ps"


# Build each group from the bottom up
for group in range(groups):

    # Create a memory controller with DRAMsim3 as the backend
    mc = sst.Component("memory_" + str(group), "memHierarchy.MemController")
    mc.addParams(mc_params)
    dram = mc.setSubComponent("backend", "memHierarchy.dramsim3")
    dram.addParams(dramsim3_params)

    # Create a Director Controller to manage the L2?


    # Create an L2 for each group
    l2 = sst.Component(l2name(group), "memHierarchy.Cache")
    l2.addParams(l2_params)

    # Create a bus to connect the L1s to the L2
    l1_l2_bus = sst.Component(busname(group), "memHierarchy.Bus")
    l1_l2_bus.addParams(bus_params)

    # Connect the bus to the L2
    link = sst.Link(linkname(busname(group), l2name(group)))
    link.connect(
        (l1_l2_bus, "low_network_0",  l1_l2_latency),
        (l2,        "high_network_0", l1_l2_latency))

    for core_id in range(cores_per_group):

        # Create an L1D for each core
        l1 = sst.Component(l1name(core_id, group), "memHierarchy.Cache")
        l1.addParams(l1_params)

        # Connect the L1 to the bus
        link = sst.Link(linkname(l1name(core_id, group), busname(group)))
        link.connect(
            (l1,        "low_network_0",                l1_l2_latency),
            (l1_l2_bus, "high_network_" + str(core_id), l1_l2_latency))


# Add the network between groups
