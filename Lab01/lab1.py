import m5
from m5.objects import *


import argparse

parser = argparse.ArgumentParser(description='A simple system with 2-level cache.')
parser.add_argument("--binary", default="/home/comparch48/gem5/tests/test-progs/hello/bin/x86/linux/hello", nargs="?", type=str,
                    help="Path to the binary to execute.")
parser.add_argument("--clock", default='1GHz', nargs='?', type=str, 
                    help="Clock rate of the CPU.")
parser.add_argument("--l1i_size", default='16kB', nargs='?', type=str, 
                    help=f"L1 instruction cache size. Default: 16kB.")
parser.add_argument("--l1d_size", default='64kB', nargs='?', type=str, 
                    help="L1 data cache size. Default: Default: 64kB.")
parser.add_argument("--l2_size", default='256kB', nargs='?', type=str, 
                    help="L2 cache size. Default: 256kB.")
parser.add_argument("--cache_line_size", default='64', nargs='?', type=str, 
                    help="Cache line size. Default: 64B.")


options = parser.parse_args()

system = System()

system.cache_line_size = options.cache_line_size

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = options.clock
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

system.cpu = X86TimingSimpleCPU()

system.membus = SystemXBar()

#system.cpu.icache_port = system.membus.cpu_side_ports
#system.cpu.dcache_port = system.membus.cpu_side_ports # the right one is an port array, and when '='ed, it will create a new port and connect to the other one.


class L1Cache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
    def connectCPU(self, cpu):
        # need to define this in a base class!
        raise NotImplementedError
    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports
    def __init__(self, options=None):
        super(L1Cache, self).__init__()
        pass

class L1ICache(L1Cache):
    size = '16kB'
    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port

    def __init__(self, options=None):
        super(L1ICache, self).__init__(options)
        if not options or not options.l1i_size:
            return
        self.size = options.l1i_size

class L1DCache(L1Cache):
    size = '64kB'
    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port
    
    def __init__(self, options=None):
        super(L1DCache, self).__init__(options)
        if not options or not options.l1d_size:
            return
        self.size = options.l1d_size

class L2Cache(Cache):
    size = '256kB'
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports
    
    def __init__(self, options=None):
        super(L2Cache, self).__init__()
        if not options or not options.l2_size:
            return
        self.size = options.l2_size

# link the cache and the CPU.

system.cpu.icache = L1ICache(options)
system.cpu.dcache = L1DCache(options)

system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

system.l2bus = L2XBar()
system.l2cache = L2Cache(options)
system.l2cache.connectCPUSideBus(system.l2bus)
system.l2cache.connectMemSideBus(system.membus)


system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)



system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports



# for gem5 V21 and beyond
system.workload = SEWorkload.init_compatible(options.binary)


process = Process()
process.cmd = [options.binary]
system.cpu.workload = process
system.cpu.createThreads()


root = Root(full_system = False, system = system)
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()

print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))





