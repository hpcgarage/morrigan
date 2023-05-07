# Automatically generated SST Python input
import sst
dramsim3_params = {
    "access_time" : "1000ns",
    "config_ini"  : "../DRAMsim3/configs/DDR3_1Gb_x8_1333.ini",
    "mem_size"    : "1GiB",
}
# Define SST core options
sst.setProgramOption("timebase", "1ps")
sst.setProgramOption("stopAtCycle", "1000000ns")

# Define the simulation components
comp_cpu = sst.Component("cpu", "prospero.prosperoCPU")
comp_cpu.addParams({
      "physlimit" : """512""",
      "tracetype" : """file""",
      "outputlevel" : """0""",
      "cache_line" : """64""",
      "file" : """traces/test-0-0.trace"""
})
reader = comp_cpu.setSubComponent("reader", "prospero.ProsperoTextTraceReader")
reader.addParams({
    "file"   : "traces/test-0-0.trace",
})
comp_l1cache = sst.Component("l1cache", "memHierarchy.Cache")
comp_l1cache.addParams({
      "access_latency_cycles" : """1""",
      "cache_frequency" : """2 Ghz""",
      "replacement_policy" : """lru""",
      "coherence_protocol" : """MSI""",
      "associativity" : """8""",
      "cache_line_size" : """64""",
      "statistics" : """1""",
      "L1" : """1""",
      "cache_size" : """64 KB"""
})
comp_memory = sst.Component("memory", "memHierarchy.MemController")
comp_memory.addParams({
      "coherence_protocol" : """MSI""",
      "system_ini" : """system.ini""",
      "clock" : """1GHz""",
      "access_time" : """1000 ns""",
      "device_ini" : """DDR3_micron_32M_8B_x4_sg125.ini""",
      "mem_size" : """512""",
})
        
memory = comp_memory.setSubComponent("backend", "memHierarchy.dramsim3")
memory.addParams(dramsim3_params)
# Define the simulation links
link_cpu_cache_link = sst.Link("link_cpu_cache_link")
link_cpu_cache_link.connect( (comp_cpu, "cache_link", "1000ps"), (comp_l1cache, "high_network_0", "1000ps") )
link_mem_bus_link = sst.Link("link_mem_bus_link")
link_mem_bus_link.connect( (comp_l1cache, "low_network_0", "50ps"), (comp_memory, "direct_link", "50ps") )
# End of generated output. 
# Enable SST Statistics Outputs for this simulation
sst.setStatisticLoadLevel(4)
sst.enableAllStatisticsForAllComponents(æ"type":"sst.AccumulatorStatistic"å)

sst.setStatisticOutput("sst.statOutputCSV")
sst.setStatisticOutputOptions( æ
    "filepath"  : "./prospero.csv",
    "separator" : ", "
    } )

