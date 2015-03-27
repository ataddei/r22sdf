from myhdl import *
from math import *

from r22sdf import *
import unittest

d=Signal(complex(1,0))
a=Signal(complex(1,0))
reset=ResetSignal(1,1,False)
clock = Signal(bool(0))
@always(delay(1))
def clkgen():
    clock.next = not clock
    return clkgen


class TestButterfly0(unittest.TestCase):

    
    def test(self):
        """Verifies butterfly r2^2 functional behavior as a serial FFT N=4"""
        self.N=4
        self.latency=self.N-1
        u_stage = stage(a,reset,clock,d,N=1)
        @instance
        def stimulus():
            for i in range(4):
                if clock:
                    reset.next = True                
                yield delay(1)
            reset.next=False
            yield delay(2)
            while True:
                yield delay(2)
        
        sim=Simulation(u_stage,clkgen,stimulus)
        
        sim.run(2)
        print "\nj,clock,reset,input,output"
        for j in range(30):
            sim.run(1,quiet=1)
            print j,clock,reset,a,d


if __name__ == '__main__':
    unittest.main()

