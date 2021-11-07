# Module for reusing params for various components

freq             = "2.0GHz"
cache_line_bytes = "256"
coherence        = "MESI"
replacement      = "lru"

l1 = {
    "access_latency_cycles" : "2",
    "cache_frequency"       : freq,
    "replacement_policy"    : replacement,
    "coherence_protocol"    : coherence,
    "associativity"         : "4",
    "cache_line_size"       : cache_line_bytes,
    "prefetcher"            : "cassini.StridePrefetcher",
    "debug"                 : "0",
    "L1"                    : "1",
    "cache_size"            : "1KiB",
}

l2 = {
    "access_latency_cycles" : "20",
    "cache_frequency"       : freq,
    "replacement_policy"    : replacement,
    "coherence_protocol"    : coherence,
    "associativity"         : "8",
    "cache_line_size"       : cache_line_bytes,
    "prefetcher"            : "cassini.StridePrefetcher",
    "debug"                 : "0",
    "L1"                    : "0",
    "cache_size"            : "2KiB",
    "mshr_latency_cycles"   : "5",
}

miranda_cpu = {
    "verbose"               : 0,
    "clock"                 : "2.0GHz",
    "printStats"            : 0,
}

miranda_3dgen = {
    "nx": 10,
    "ny": 10,
    "nz": 10,
}

memctrl = {
    "clock" : freq,
    "addr_range_end" : 4096 * 1024 * 1024 - 1
}

simplemem = {
    "access_time" : "100 ns",
    "mem_size" : "4096MiB",
}
