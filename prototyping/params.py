# Module for reusing params for various components

freq             = "2.0GHz"
cache_line_bytes = "256"
coherence        = "MESI"
replacement      = "lru"

class DCParam:
    def __init__(self, ngroup, mem_per_group=1*1024*1024*1024, interleave_size=4*1024):
        self.ngroup = ngroup
        self.mem_per_group = mem_per_group
        self.interleave_size = interleave_size
        self.capacity = ngroup * mem_per_group

    def __getitem__(self, idx):
        if (idx < 0 or idx > ngroup-1):
            raise IndexError("Index out of range: {}".format(idx))
        return {
            # Per-Group Params
            "addr_range_start" : idx*interleave_size,
            "addr_range_end"   : self.capacity - (self.ngroup-idx-1)*self.interleave_size - 1,
            "interleave_size"  : self.interleave_size,
            "interleave_step"  : self.ngroup * self.interleave_size,
            # Global Params
            #TODO what is the entry cache? Different from mshr?
            "clock"                  : freq,
            "coherence_protocol"     : coherence,
            "entry_cache_size"       : "256*1024*1024",
            "mshr_num_entries"       : 128,
            "access_latency_cycles"  : 2,
            "cache_line_size"        : cache_line_bytes,
        }

class Param:
    def __init__(self, ngroup):
        self.ngroup = ngroup
        self.dc = DCParam(ngroup)

        self.l1 = {
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

        self.l2 = {
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

l3 = {
    "access_latency_cycles" : "100",
    "cache_frequency"       : freq,
    "replacement_policy"    : replacement,
    "coherence_protocol"    : coherence,
    "associativity"         : "8",
    "cache_line_size"       : cache_line_bytes,
    "prefetcher"            : "cassini.StridePrefetcher",
    "debug"                 : "0",
    "L1"                    : "0",
    "cache_size"            : "32KiB",
    "mshr_latency_cycles"   : "10",
}

miranda_cpu = {
    "verbose"               : 0,
    "clock"                 : freq,
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

dramsim3 = {
    "config_ini"  : "../DRAMsim3/configs/DDR3_1Gb_x8_1333.ini",
    "mem_size"    : "1GiB",
}

bus = {
    "bus_frequency" : freq,
}

# TODO: Do I need to set the accept_region? Not on the l1l2 link, right?
# TODO: Do I even need a memlink there?
memlink = {
    #nothing
}

linkcontrol = {

}

#TODO figure out groups. Will the mem controllers send to each other? The DC will, I think.
dcnic = {
    "group":"0",
    "sources":"0,1",
    "dest":"0,1",
}

l2nic = {
    "group":"1",
    "sources":"1",
    "dest":"0"
}

# linkcontrol, grid
