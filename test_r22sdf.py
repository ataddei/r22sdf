from myhdl import *
from math import *
from numpy import *
from r22sdf import *
import unittest
from random import *
## d=Signal(complex(1,0))
## a=Signal(complex(1,0))
## reset=ResetSignal(1,1,False)
## clock = Signal(bool(0))
## @always(delay(1))
## def clkgen():
##     clock.next = not clock
##     return clkgen


class TestDefault(unittest.TestCase):

    def setUp(self):
        self.N=4
        self.latency=self.N-1
        self.collect=[]
        self.a=Signal(complex(0,0))
        self.d=Signal(complex(0,0))
        self.reset=ResetSignal(1,1,False)
        self.clock = Signal(bool(0))
        self.uut = stage(self.a,self.reset,self.clock,self.d,N=1)
        self.gg=self.input_generator()
    def input_generator(self):
        self.inputs=[complex(1,0) for i in range(self.N)]*2
        for i in self.inputs:
            yield i

    def runTest(self):
        """Verifies butterfly r2^2 functional behavior as a serial FFT N=4"""
        @always(delay(1))
        def clkgen():
            self.clock.next = not self.clock        
        @instance
        def stimulus():
            self.reset.next = True
            self.a.next=next(self.gg)
            for i in range(self.N):
                yield delay(1)
            yield delay(1)
            self.reset.next=False
            while True:
                if (self.reset==False and self.clock==True):
                    self.a.next=next(self.gg)
                    self.collect.append(self.d.val)                    
                yield delay(1)
        sim=Simulation(self.uut,clkgen,stimulus)
        for j in range(20):
            sim.run(1,quiet=1)
        self.check()
    def check(self):
        self.assertListEqual(list(fft.fft(self.inputs[0:self.N])),self.collect[self.latency-1:self.latency-1+self.N])

class TestDefaultRandomReal(TestDefault):
    def input_generator(self):
        self.inputs=[complex(random(),random()) for i in range(self.N)]*2
        for i in self.inputs:
            yield i


if __name__ == '__main__':
    unittest.main()

