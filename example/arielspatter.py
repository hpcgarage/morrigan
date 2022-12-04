import sst
import os

sst.setProgramOption("timebase", "1ps")

stream_app = os.getenv("ARIEL_TEST_STREAM_APP")
if stream_app == None:
    sst_root = os.getenv( "SST_ROOT" )
    app = sst_root + "/sst-elements/src/sst/elements/ariel/frontend/simple/examples/stream/stream"
else:
    app = stream_app

if not os.path.exists(app):
    app = os.getenv( "OMP_EXE" )

ariel = sst.Component("a0", "ariel.ariel")
ariel.addParams({
        "verbose" : "0",
        "maxcorequeue" : "256",
        "maxissuepercycle" : "2",
        "pipetimeout" : "0",
        "executable" : "../../spatter/build_omp_gnu/./spatter",
        "appargcount": 1,
        "apparg0": "-pUNIFORM:8:1",
        "arielmode" : "1",
        "launchparamcount" : 1,
        "launchparam0" : "-ifeellucky",
        })
        #stats at the moment - 8 bytes per pattern (some have 4?) - need to figure out why there are read requests and write, should only be read 
memmgr = ariel.setSubComponent("memmgr", "ariel.MemoryManagerSimple")


corecount = 1

l1cache = sst.Component("l1cache", "memHierarchy.Cache")
l1cache.addParams({
    "L1" : 1,
    "cache_frequency" : "2.4GHz",
    "access_latency_cycles" : 2,
    "cache_size" : "2KiB",
    "associativity" : 4,
    "replacement_policy" : "lru",
    "coherence_policy" : "MESI",
    "cache_line_size" : 64,
    "prefetcher": "cassini.StridePrefetcher",
    "reach": 16,
    "detect_range": 1
})

memctrl = sst.Component("memory", "memHierarchy.MemController")
memctrl.addParams({
        "clock" : "1GHz",
})

memory = memctrl.setSubComponent("backend", "memHierarchy.simpleMem")
memory.addParams({
        "mem_size" : "1GiB",
        "access_time" : "50ns",
})

cpu_cache_link = sst.Link("cpu_cache_link")
cpu_cache_link.connect( (ariel, "cache_link_0", "50ps"), (l1cache, "high_network_0", "50ps") )

memory_link = sst.Link("mem_bus_link")
memory_link.connect( (l1cache, "low_network_0", "50ps"), (memctrl, "direct_link", "50ps") )


# Set the Statistic Load Level; Statistics with Enable Levels (set in
# elementInfoStatistic) lower or equal to the load can be enabled (default = 0)
sst.setStatisticLoadLevel(10)
sst.enableAllStatisticsForAllComponents({"type":"sst.AccumulatorStatistic"})

sst.setStatisticOutput("sst.statOutputCSV", {"filepath" : "./ArielStream.csv",
                                                         "separator" : ", "
                                            })

# Enable Individual Statistics for the Component with output at end of sim
# Statistic defaults to Accumulator
