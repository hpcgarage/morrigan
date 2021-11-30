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
        if (idx < 0 or idx > self.ngroup-1):
            raise IndexError("Index out of range: {}".format(idx))
        return {
            # Per-Group Params
            "addr_range_start" : idx*self.interleave_size,
            "addr_range_end"   : self.capacity - (self.ngroup-idx-1)*self.interleave_size - 1,
            "interleave_size"  : str(self.interleave_size) + "B",
            "interleave_step"  : str(self.ngroup * self.interleave_size) + "B",
            # Global Params
            #TODO what is the entry cache? Different from mshr?
            "clock"                  : freq,
            "coherence_protocol"     : coherence,
            "entry_cache_size"       : "256*1024*1024",
            "mshr_num_entries"       : 128,
            "access_latency_cycles"  : 2,
            "cache_line_size"        : cache_line_bytes,
        }

class MemCtrlParam:
    def __init__(self, ngroup, mem_per_group=1*1024*1024*1024, interleave_size=4*1024):
        self.ngroup = ngroup
        self.mem_per_group = mem_per_group
        self.interleave_size = interleave_size
        self.capacity = ngroup * mem_per_group

    def __getitem__(self, idx):
        if (idx < 0 or idx > self.ngroup-1):
            raise IndexError("Index out of range: {}".format(idx))
        return {
            # Per-Group Params
            "addr_range_start" : idx*self.interleave_size,
            "addr_range_end"   : self.capacity - (self.ngroup-idx-1)*self.interleave_size - 1,
            "interleave_size"  : str(self.interleave_size) + "B",
            "interleave_step"  : str(self.ngroup * self.interleave_size) + "B",
            # Global Params
            "clock"   : freq, #TODO: what freq to use?
            "backing" : "none",
        }

class Param:
    def __init__(self, ncpu, ngroup, exe, args):
        self.ngroup  = ngroup
        self.dc      = DCParam(ngroup)
        self.memctrl = MemCtrlParam(ngroup)

        self.ariel   = {
            "verbose"        : 0,
            "corecount"      : ncpu,
            "cachelinesize"  : 256,
            "executable"     : exe,
            "appargcount"    : len(args),
            "envparamcount"  : 1,
            "envparamname0"  : "OMP_NUM_THREADS",
            "envparamval0"   : str(ncpu),
            "clock"          : "2.0GHz",
            "arielmode"      : 0,
        }

        for i in range(len(args)):
            self.ariel["apparg" + str(i)] = args[i]

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

        self.dramsim3 = {
            "config_ini"  : "../DRAMsim3/configs/DDR3_1Gb_x8_1333.ini",
            "mem_size"    : "1GiB",
        }

        self.bus = {
            "bus_frequency" : freq,
        }

        # TODO: Do I need to set the accept_region? Not on the l1l2 link, right?
        # TODO: Do I even need a memlink there?
        self.memlink = {
            #nothing
        }


        self.mesh_flit           = 36
        self.mesh_link_latency   = "100ps"
        self.freq_mhz            = 2000 #TODO:  use 2200MHz?
        self.mesh_link_bw        = str( (self.freq_mhz*1000*1000*self.mesh_flit) ) + "B/s"
        self.network_buffers     = "288B"
        self.noc = {
                "link_bw" : self.mesh_link_bw,
                "flit_size" : str(self.mesh_flit) + "B",
                "input_buf_size" : self.network_buffers,
                "port_priority_equal" : 1,
        }

        self.linkcontrol = {
            "link_bw"      : self.mesh_link_bw,
            "in_buf_size"  : self.network_buffers,
            "out_buf_size" : self.network_buffers,
        }
        #TODO figure out groups. Will the mem controllers send to
        #each other? The DC will, I think.

        self.dcnic = {
            "group":"0",
            "sources":"0,1",
            "dest":"0,1",
        }

        self.l2nic = {
            "group":"1",
            "sources":"0,1",
            "dest":"0,1"
        }



# linkcontrol, noc
