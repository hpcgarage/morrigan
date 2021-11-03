# Information is pulled from
# [ds.N] Page N of the A64FX (d)ata(s)heet, located in this directory at a64fx-datashee.pdf
# [mm.N] Page N of the A64FX (m)icroarchitecture (m)anual, located at a64fx-microarchitecture-manual.pdf

import sst
import os

next_core_id = 0
next_network_id = 0
next_memory_ctrl_id = 0

clock = "2000MHz"           # [ds.2] - Choose from 1.9, 2.0, or 2.1 GHz
memory_clock = "200MHz"
coherence_protocol = "MESI" # [mm.64] - The L1D and the L2 both use MESI. The L1I uses SI

# The Fujitsu A64FX has 13 cores per group but 1 is used for management.
# TODO: Use inactive cores for programs running with less than all 48 threads
cores_per_group = 12
active_cores_per_group = 12
memory_controllers_per_group = 1
groups = 4

os.environ["OMP_NUM_THREADS"]=str(groups * cores_per_group)

# TODO: Remove all references to L3. The A64FX has no L3 cache.

#l3cache_blocks_per_group = 5
#l3cache_block_size = "1MB"

ring_latency = "50ps"
ring_bandwidth = "85GB/s"
ring_flit_size = "72B"

memory_network_bandwidth = "85GB/s"

mem_interleave_size = 4096      # Do 4K page level interleaving
memory_capacity = 16384         # Size of memory in MBs

streamN = 1000000

l1_prefetch_params = {
        }

l2_prefetch_params = {
    "prefetcher": "cassini.StridePrefetcher",
    "reach": 16,
    "detect_range" : 1
}

ringstop_params = {
    "torus:shape" : groups * (cores_per_group + memory_controllers_per_group + l3cache_blocks_per_group),
    "output_latency" : "100ps",
    "xbar_bw" : ring_bandwidth,
    "input_buf_size" : "2KB",
    "input_latency" : "100ps",
    "num_ports" : "3",
    "debug" : "0",
    "torus:local_ports" : "1",
    "flit_size" : ring_flit_size,
    "output_buf_size" : "2KB",
    "link_bw" : ring_bandwidth,
    "torus:width" : "1",
    "topology" : "merlin.torus"
}

topology_params = {
    "shape" : groups * (cores_per_group + memory_controllers_per_group + l3cache_blocks_per_group),
    "local_ports" : "1",
    "width" : "1",
}

#TODO  the latencies given in [mm] for the l1 and l2 are "load-to-use" latencies. How should I adjust the access latencies for SST. Do I need
#subtract off cycles of overhead in the simulator?
# TODO does ariel track dependencies between instructions?

#TODO the indexing method is given for these caches on [mm.64-65]. Where do I use this?

# [mm.12] Each L1I is 64KiB, 4-way associative
l1_params = {
    "coherence_protocol"   : coherence_protocol,
    "cache_frequency"      : clock,
    "replacement_policy"   : "lru",   # assumed LRU based on sector cache description in [mm.78]
    "cache_size"           : "64KiB",
    "maxRequestDelay"      : "10000",   #Note - originally was 1000000ns
    "associativity"        : 4,
    "cache_line_size"      : 256,
    "access_latency_cycles": 5,    # [mm.64] - 5 is minimum, longer for sve
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
}

memctrl_params = {
    "backing": "none",       # we do not require correct memory values
    "clock"  : memory_clock, # TODO
}

dramsim3_params = {
    "config_ini"  : "../../DRAMsim3/configs/HBM2_8Gb_x128.in",
    "mem_size"    : "8GiB"
}

##########################
#TODO - everything below #
##########################
dc_params = {
    "coherence_protocol": coherence_protocol,
    "memNIC.network_bw": memory_network_bandwidth,
    "memNIC.interleave_size": str(mem_interleave_size) + "B",
    "memNIC.interleave_step": str((groups * memory_controllers_per_group) * mem_interleave_size) + "B",
    "entry_cache_size": 256*1024*1024, #Entry cache size of mem/blocksize
    "clock": memory_clock,
    "debug": 1,
}

print("Configuring Ariel processor model (" + str(groups)" CMGs with "str(cores_per_group) + " cores each)...")

ariel = sst.Component("A0", "ariel.ariel")
ariel.addParams({ #TODO
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
})

memmgr = ariel.setSubComponent("memmgr", "ariel.MemoryManagerSimple")
memmgr.addParams({
    "memmgr.pagecount0"   : "1048576",
})

router_map = {}

# Some Notes From [mm.63]
# - The L2 caches are interconnected by two-way ring bus
# - The L2 caches are inclusive
# - Each L1I contains a MIB (Move In Buffer) to manage in-flight rquests to the MAC
# - Each L1D contains an MIB and a MOB (Move Out Buffer) as well. These structures asynchrnously manage requests
# - [mm.64] Top of the page contains throughputs for all of these buffers in bytes/cycle
# - MIB/MOB defined in 9.4

print("Configuring ring network...")

# Loop over each core and eacjh l3 cache block. Each one gets a ring stop, which is a merlin.hr_router
# Each one gets added to the 

# Create a merlin.hr_router for each core, for each cache block, and for each memory controller
# add each to the router_map
for next_ring_stop in range((cores_per_group + memory_controllers_per_group + l3cache_blocks_per_group) * groups):
    ring_rtr = sst.Component("rtr." + str(next_ring_stop), "merlin.hr_router")
    ring_rtr.addParams(ringstop_params)
    ring_rtr.addParams({
        "id" : next_ring_stop
    })
    topo = ring_rtr.setSubComponent("topology","merlin.torus")
    topo.addParams(topology_params)
    router_map["rtr." + str(next_ring_stop)] = ring_rtr

# Create the ring topology by connecting each ring_stop with the next
for next_ring_stop in range((cores_per_group + memory_controllers_per_group + l3cache_blocks_per_group) * groups):
    if next_ring_stop == ((cores_per_group + memory_controllers_per_group + l3cache_blocks_per_group) * groups) - 1:
        rtr_link = sst.Link("rtr_" + str(next_ring_stop))
        rtr_link.connect( (router_map["rtr." + str(next_ring_stop)], "port0", ring_latency), (router_map["rtr.0"], "port1", ring_latency) )
    else:
        rtr_link = sst.Link("rtr_" + str(next_ring_stop))
        rtr_link.connect( (router_map["rtr." + str(next_ring_stop)], "port0", ring_latency), (router_map["rtr." + str(next_ring_stop+1)], "port1", ring_latency) )


# Loop over each group
for next_group in range(groups):
    print("Configuring core and memory controller group " + str(next_group) + "...")

#For each core in a group
#   Give each its own L1 and L2
#   Link the ariel core with the L1, and link the L1 with the L2
#   Link the L2 with the ring
    for next_active_core in range(active_cores_per_group):
        print("Creating active core " + str(next_active_core) + " in group " + str(next_group))

        l1 = sst.Component("l1cache_" + str(next_core_id), "memHierarchy.Cache")
        l1.addParams(l1_params)
        l1.addParams(l1_prefetch_params)

        l2 = sst.Component("l2cache_" + str(next_core_id), "memHierarchy.Cache")
        l2.addParams(l2_params)
        l2.addParams(l2_prefetch_params)

        ariel_cache_link = sst.Link("ariel_cache_link_" + str(next_core_id))
        ariel_cache_link.connect( (ariel, "cache_link_" + str(next_core_id), ring_latency), (l1, "high_network_0", ring_latency) )

        l2_core_link = sst.Link("l2cache_" + str(next_core_id) + "_link")
        l2_core_link.connect((l1, "low_network_0", ring_latency), (l2, "high_network_0", ring_latency))

        l2_ring_link = sst.Link("l2_ring_link_" + str(next_core_id))
        l2_ring_link.connect((l2, "cache", ring_latency), (router_map["rtr." + str(next_network_id)], "port2", ring_latency))

        next_network_id = next_network_id + 1
        next_core_id = next_core_id + 1

# Do exactly the same as the preious loop but for inactive cores
    for next_inactive_core in range(cores_per_group - active_cores_per_group):
        print("Creating inactive core: " + str(next_inactive_core) + " in group " + str(next_group))

        l1 = sst.Component("l1cache_" + str(next_core_id), "memHierarchy.Cache")
        l1.addParams(l1_params)
        l1.addParams(l1_prefetch_params)

        l2 = sst.Component("l2cache_" + str(next_core_id), "memHierarchy.Cache")
        l2.addParams(l2_params)
        l2.addParams(l2_prefetch_params)

        ariel_cache_link = sst.Link("ariel_cache_link_" + str(next_core_id))
        ariel_cache_link.connect( (ariel, "cache_link_" + str(next_core_id), ring_latency), (l1, "high_network_0", ring_latency) )

        l2_core_link = sst.Link("l2cache_" + str(next_core_id) + "_link")
        l2_core_link.connect((l1, "low_network_0", ring_latency), (l2, "high_network_0", ring_latency))

        l2_ring_link = sst.Link("l2_ring_link_" + str(next_core_id))
        l2_ring_link.connect((l2, "cache", ring_latency), (router_map["rtr." + str(next_network_id)], "port2", ring_latency))

        next_network_id = next_network_id + 1
        next_core_id = next_core_id + 1

# For each L3 cache block in the group,
#   Create a memHierarchy.Cache object
#   Connect it to the ring
    for next_l3_cache_block in range(l3cache_blocks_per_group):
        print("Creating L3 cache block: " + str(next_l3_cache_block) + " in group: " + str(next_group))

        l3cache = sst.Component("l3cache" + str((next_group * l3cache_blocks_per_group) + next_l3_cache_block), "memHierarchy.Cache")
        l3cache.addParams(l3_params)

        l3cache.addParams({
            "slice_id" : str((next_group * l3cache_blocks_per_group) + next_l3_cache_block)
        })

        l3_ring_link = sst.Link("l3_ring_link_" + str((next_group * l3cache_blocks_per_group) + next_l3_cache_block))
        l3_ring_link.connect( (l3cache, "directory", ring_latency), (router_map["rtr." + str(next_network_id)], "port2", ring_latency) )

        next_network_id = next_network_id + 1

# For each mem controler in the group
#   Compute local size as the total capacity divided by the number of groups times the number of controllers in a group
#   TODO: this means I need to adjust the memory_capacity above be the capacity of the whole system, not a single CMG?
#   Add a dramsim3 module as the backend for each memory controller
#   set a mH.DirectoryController for each and give it a range of addresses to watch for
#   link the directory controller with the memory controller
#   link the directory controller with a ringstop
    for next_mem_ctrl in range(memory_controllers_per_group):
        local_size = memory_capacity // (groups * memory_controllers_per_group)

        memctrl = sst.Component("memory_" + str(next_memory_ctrl_id), "memHierarchy.MemController")
        memctrl.addParams(memctrl_params)
        memory = memctrl.setSubComponent("backend", "memHierarchy.dramsim3")
        memory.addParams(dramsim3_params)

        dc = sst.Component("dc_" + str(next_memory_ctrl_id), "memHierarchy.DirectoryController")
        dc.addParams({
            "memNIC.addr_range_start" : next_memory_ctrl_id * mem_interleave_size,
            "memNIC.addr_range_end" : (memory_capacity * 1024 * 1024) - (groups * memory_controllers_per_group * mem_interleave_size) + (next_memory_ctrl_id * mem_interleave_size)
        })
        dc.addParams(dc_params)

        memLink = sst.Link("mem_link_" + str(next_memory_ctrl_id))
        memLink.connect((memctrl, "direct_link", ring_latency), (dc, "memory", ring_latency))

        netLink = sst.Link("dc_link_" + str(next_memory_ctrl_id))
        netLink.connect((dc, "network", ring_latency), (router_map["rtr." + str(next_network_id)], "port2", ring_latency))

        next_network_id = next_network_id + 1
        next_memory_ctrl_id = next_memory_ctrl_id + 1

# Enable SST Statistics Outputs for this simulation
sst.setStatisticLoadLevel(4)
sst.enableAllStatisticsForAllComponents({"type":"sst.AccumulatorStatistic"})

sst.setStatisticOutput("sst.statOutputCSV")
sst.setStatisticOutputOptions( {
    "filepath"  : "./stats-fuji.csv",
    "separator" : ", "
} )

print("Completed configuring the A64FX model")
