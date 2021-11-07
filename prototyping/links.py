import sst

l2_params = {
    "coherence_protocol"   : "MSI",
    "cache_frequency"      : "200MHz",
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

miranda_params = {
    "clock" : "2.0GHz",
}

stream_params = {
    "verbose" : 0,
    "n" : 10,
    "operandwidth" : 16,
}

component_count = {}

def anon(component, params={}):
    if component in component_count:
        num = component_count[component]
        component_count[component] = num + 1
    else:
        num = 0
        component_count[component] = 1

    name = "_" + component + "_" + str(num)
    comp = sst.Component(name, component)
    comp.addParams(params)
    return comp

def miranda_core(params, genid, gen_params):
   core = anon("miranda.BaseCPU", params)
   gen = core.setSubComponent("generator", genid)
   gen.addParams(gen_params)
   return core


mc_params = {
      "clock" : "1GHz",
      "addr_range_end" : 4096 * 1024 * 1024 - 1
}
mem_backend_params = {
      "access_time" : "100 ns",
      "mem_size" : "4096MiB",
}


def memory(params, backend, backend_params):
    mem = anon("memHierarchy.MemController", params)
    backend = mem.setSubComponent("backend", backend)
    backend.addParams(backend_params)
    return mem

####################
# BUILD SIMULATION #
####################

cpu = miranda_core(miranda_params, "miranda.STREAMBenchGenerator", stream_params)

#l1  = anon("memHierarchy.Cache", l2_params)

mem = memory(mc_params, "memHierarchy.simpleMem", mem_backend_params)

link = sst.Link("cpu_to_mem")
link.connect( (cpu,"cache_link","1000ps"), (mem,"direct_link", "50ps") )

print(component_count)

#link = sst.Link("link1")
#comp = sst.Component("mem", "memHierarchy.Cache")
#comp.addParams(l2_params)
#print(comp.getFullName())
