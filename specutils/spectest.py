import sst
from ariel_utils import parseAriel



# Utility method
def mklink(e1, e2):
      link = sst.Link("link_" + e1[0].getFullName() + "[" + e1[1] + "]" + "_" +
                                e2[0].getFullName() + "[" + e2[1] + "]" )
      link.connect(e1, e2)
      return link

#ariel_command = "ls -al"
#ariel_command = "./adder < numbers.txt 2>>err.txt"
ariel_command = "MYENVVAR=20 ./adder < numbers.txt > out.txt 2>> err.txt"

# Components
core    = sst.Component("Ariel", "ariel.ariel")
#gen     = core.setSubComponent("generator", "miranda.CopyGenerator")
l1      = sst.Component("L1Cache", "memHierarchy.Cache")
memctrl = sst.Component("MemoryController", "memHierarchy.MemController")
backend = memctrl.setSubComponent("backend", "memHierarchy.simpleMem")

# Parameters
freq="2GHz"
#################NOTE - Change arielmode to 1 for spec (unless you find a way to add the ariel_enable call)
core.addParams({"clock":freq, "arielmode":1})
#core.addParams(parseAriel(ariel_command))
core.addParams({'executable': '/home/plavin3/spec/spec2017/benchspec/CPU/641.leela_s/run/run_base_test_mrgn-m64.0000/../run_base_test_mrgn-m64.0000/leela_s_base.mrgn-m64', 'appargcount': 1, 'apparg0': 'test.sgf', 'appstdout': 'test.out', 'appstdoutappend': 0, 'appstderr': 'test.err', 'appstderrappend': 1})

#gen.addParams({"request_count":20})
l1.addParams({"l1":"true", "cache_frequency":freq, "cache_size":"1KiB", "associativity":4, "access_latency_cycles":2, "L1":"true"})
memctrl.addParams({"clock":freq, "backing":"none", "addr_range_end":1024**3-1})
backend.addParams({"mem_size":"1GiB"})

# Links
latency="1000ps"
mklink((core, "cache_link_0", latency),  (l1, "high_network_0", latency))
mklink((l1, "low_network_0", latency), (memctrl, "direct_link", latency))

# Satatistics
l1.enableStatistics(["GetS_recv","CacheHits", "CacheMisses","TotalEventsReceived","MSHR_occupancy" ])
core.enableStatistics(["split_read_reqs"])

# Define SST core options
sst.setProgramOption("timebase", "1ps")
sst.setStatisticLoadLevel(9)
#sst.enableAllStatisticsForAllComponents()

sst.setStatisticOutput("sst.statOutputCSV", {"filepath" : "./spectest_stats.csv", "separator" : ", " } )

# stats
