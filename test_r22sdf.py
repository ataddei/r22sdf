from myhdl import *
from math import *
from numpy import *
from r22sdf import *
import unittest
from random import *

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
    def tearDown(self):
        self.N       =[]
        self.latency =[]
        self.collect =[]
        self.a       =[]
        self.d       =[]
        self.reset   =[]
        self.clock   =[]
        self.uut     =[]
        self.gg      =[]

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
            '''Driving stimulus in positive cycle and strobing in negative cycle to avoid race coinditions'''
            while True:                        
                yield delay(1)
        @always(self.clock.posedge)
        def stim():
            if (self.reset==False):
                self.a.next= next(self.gg)
        @always(self.clock.negedge)
        def strobe():
            if (self.reset==False):
                self.collect.append(self.d.val)
        
                
        sim=Simulation(self.uut,clkgen,stimulus,stim,strobe)
        for j in range(20):
            sim.run(1,quiet=1)
        self.check()
    def check(self):
        '''Checks sorted values'''
        self.assertListEqual(list(sort(fft.fft(self.inputs[0:self.N]))),list(sort(self.collect[self.latency-1:self.latency-1+self.N])))

class TestDefaultRandomReal(TestDefault):
    def input_generator(self):
        self.inputs=[complex(random(),0) for i in range(self.N)]*2
        for i in self.inputs:
            yield i

class TestDefaultZero(TestDefault):
    def input_generator(self):
        self.inputs=[complex(0,0) for i in range(self.N)]*2
        for i in self.inputs:
            yield i
class TestDefaultImpulse0(TestDefault):
    def input_generator(self):
        self.inputs=[complex(random(),random()) if i==0 else complex(0,0) for i in range(self.N)]*2
        for i in self.inputs:
            yield i
class TestDefaultImpulse1(TestDefault):
    def input_generator(self):
        self.inputs=[complex(random(),random()) if i==1 else complex(0,0) for i in range(self.N)]*2
        for i in self.inputs:
            yield i
class TestDefaultImpulse2(TestDefault):
    def input_generator(self):
        self.inputs=[complex(1,0) if i==2 else complex(0,0) for i in range(self.N)]*2
        for i in self.inputs:
            yield i
class TestDefaultImpulse3(TestDefault):
    def input_generator(self):
        self.inputs=[complex(random(),0) if i==3 else complex(0,0) for i in range(self.N)]*2
        for i in self.inputs:
            yield i

if __name__ == '__main__':
    unittest.main()

