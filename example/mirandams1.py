import sst

#########################################################################
## Define SST core options
#########################################################################
sst.setProgramOption("stopAtCycle", "100ms") 


#########################################################################
## Declare components
#########################################################################
core = sst.Component("core", "miranda.BaseCPU")
cache = sst.Component("cache", "memHierarchy.Cache")
memctrl = sst.Component("memory", "memHierarchy.MemController")


#########################################################################
## Set component parameters and fill subcomponent slots
#########################################################################
# Core: 2.4GHz, 2 accesses/cycle,  
core.addParams({
    "clock" : "2.4GHz",
    "max_reqs_cycle" : 2,
})
gen = core.setSubComponent("generator", "miranda.SingleStreamGenerator")

gen.addParams({
    "gapJump" : 32,
    "gaplocations" : 4,
})


# Cache: L1, 2.4GHz, 2KB, 4-way set associative, 64B lines, LRU replacement, MESI coherence
cache.addParams({
    "L1" : 1,
    "cache_frequency" : "2.4GHz",
    "access_latency_cycles" : 2,
    "cache_size" : "2KiB",
    "associativity" : 4,
    "replacement_policy" : "lru",
    "coherence_policy" : "MESI",
    "cache_line_size" : 64,
})

# Memory: 50ns access, 1GB
memctrl.addParams({
    "clock" : "1GHz",
    "backing" : "none"
})
memory = memctrl.setSubComponent("backend", "memHierarchy.simpleMem")
memory.addParams({
    "mem_size" : "1GiB",
    "access_time" : "50ns",
})


#########################################################################
## Declare links
#########################################################################
core_cache = sst.Link("core_to_cache")
cache_mem = sst.Link("cache_to_memory")


#########################################################################
## Connect components with the links
#########################################################################
core_cache.connect( (core, "cache_link", "100ps"), (cache, "high_network_0", "100ps") )
cache_mem.connect( (cache, "low_network_0", "100ps"), (memctrl, "direct_link", "100ps") )

################################ Stats ################################
sst.setStatisticLoadLevel(2)
sst.enableAllStatisticsForAllComponents({"type":"sst.AccumulatorStatistic"})

sst.setStatisticOutput("sst.statOutputCSV")
sst.setStatisticOutputOptions( {
    "filepath" : "./stats-miranda.csv",
    "seperator" : ", "
})

################################ The End ################################