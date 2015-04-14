from myhdl import *
from math import *
from numpy import *
from r22sdf import *
import unittest
from random import *
import pdb

class TestDefault(unittest.TestCase):

    def setUp(self):
        self.N=4
        self.latency=self.N-1
        self.collect=[]
        self.a=Signal(complex(0,0))
        self.d=Signal(complex(0,0))
        self.reset=ResetSignal(1,1,False)
        self.clock = Signal(bool(0))
        self.uut = r22sdf_top(self.a,self.reset,self.clock,self.d,N=1)
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
                yield delay(1)
        @always(self.clock.posedge)
        def stim():
            if (self.reset==False):
                self.a.next= next(self.gg)
        @always(self.clock.negedge)
        def fetch():
            if (self.reset==False):
                self.collect.append(self.d.val)
        
                
        sim=Simulation(self.uut,clkgen,stimulus,stim,fetch)
        for j in range(8*self.N):
            sim.run(1,quiet=1)
        self.check()
    def check(self):
        '''Checks sorted values'''        
        self.fft_reference = list(sort_complex(fft.fft(self.inputs[0:self.N])))
        self.fft_test      = list(sort_complex(self.collect[self.latency-1:self.latency-1+self.N]))
        self.fft_reference_r = [i.round(8) for i in self.fft_reference]
        self.fft_test_r      = [i.round(8) for i in self.fft_test]
        #print self.fft_test,self.fft_reference
        self.assertListEqual(self.fft_reference_r,self.fft_test_r)
       
class TestDefaultRandomReal(TestDefault):
    def input_generator(self):
        self.inputs=[complex128(complex(random(),0.0)).round(8) for i in range(self.N)]*2
        for i in self.inputs:
            yield i
class TestDefaultRandom(TestDefault):
    def input_generator(self):
        self.inputs=[complex128(complex(round(random()-0.5,5),round(random()-0.5,5))).round(8) for i in range(self.N)]*2
        for i in self.inputs:
            yield i

class TestDefaultZero(TestDefault):
    def input_generator(self):
        self.inputs=[complex(0,0) for i in range(self.N)]*2
        for i in self.inputs:
            yield i
class TestDefaultImpulse0(TestDefault):
    def input_generator(self):
        self.inputs=[(complex(random(),random())) if i==0 else complex(0,0) for i in range(self.N)]*2
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

class TestDefaultFFT (TestDefault):
    def setUp(self):
        self.N=16
        self.latency=self.N-1
        self.collect=[]
        self.a=Signal(complex(0,0))
        self.d=Signal(complex(0,0))
        self.reset=ResetSignal(1,1,False)
        self.clock = Signal(bool(0))
        self.uut = r22sdf_top(self.a,self.reset,self.clock,self.d,N=2)
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


class TestDefaultFFTZero(TestDefaultFFT):
    def input_generator(self):
        self.inputs=[complex(0,0) for i in range(self.N)]*2
        for i in self.inputs:
            yield i
class TestDefaultFFTImpulse0(TestDefaultFFT):
    def input_generator(self):
        self.inputs=[(complex(random(),random())) if i==0 else complex(0,0) for i in range(self.N)]*2
        for i in self.inputs:
            yield i

class TestDefaultFFTImpulse1(TestDefaultFFT):
    def input_generator(self):
        self.inputs=[complex(random(),random()) if i==1 else complex(0,0) for i in range(self.N)]*2
        for i in self.inputs:
            yield i
class TestDefaultFFTImpulse2(TestDefaultFFT):
    def input_generator(self):
        self.inputs=[complex(1,0) if i==2 else complex(0,0) for i in range(self.N)]*2
        for i in self.inputs:
            yield i
class TestDefaultFFTImpulse3(TestDefaultFFT):
    def input_generator(self):
        self.inputs=[complex(random(),0) if i==3 else complex(0,0) for i in range(self.N)]*2
        for i in self.inputs:
            yield i
class TestDefaultFFTImpulse3(TestDefaultFFT):
    def input_generator(self):
        self.inputs=[complex(random(),0) if i==3 else complex(0,0) for i in range(self.N)]*2
        for i in self.inputs:
            yield i
class TestDefaultFFTImpulseRandom(TestDefaultFFT):
    def input_generator(self):
        imp=[randint(0,self.N-1), randint(0,self.N-1) ]
        imp=[3,4]
        print imp
        self.inputs=[complex(1,0) if i in imp else complex(0,0) for i in range(self.N)]*2
        for i in self.inputs:
            yield i
class TestDefaultFFTRandom(TestDefaultFFT):
    def input_generator(self):
        self.inputs=[complex128(complex(round(random()-0.5,5),round(random()-0.5,5))).round(8) for i in range(self.N)]*2
        for i in self.inputs:
            yield i

class TestDefaultFFTSaw(TestDefaultFFT):
    def input_generator(self):
        self.inputs=[complex128(complex(i,i)).round(8) for i in range(self.N)]*2
        for i in self.inputs:
            yield i

class TestDefaultFFTRandomImpulseSweep(TestDefaultFFTImpulseRandom):
    def setUp(self,idx=0):
        self.N=16
        self.latency=self.N-1
        self.collect=[]
        self.a=Signal(complex(0,0))
        self.d=Signal(complex(0,0))
        self.reset=ResetSignal(1,1,False)
        self.clock = Signal(bool(0))
        self.uut = r22sdf_top(self.a,self.reset,self.clock,self.d,N=2)
        self.idx=idx
        self.inputs=[complex(1,0) if i == idx else complex(0,0) for i in range(self.N)]*2
        self.gg=self.input_generator()

    def input_generator(self):        
        for i in self.inputs:
            yield i
    def runTest(self):
        self.setUp()
        self.count=[]
        for i in range(16):
            try:
                self.setUp(i)
                super(TestDefaultFFTRandomImpulseSweep,self).runTest()
                self.tearDown()
            except Exception as e:
                #print e,"Exception Failed in: ",self.idx
                self.count.append(i)
        if len(self.count)>0:
            print "Failing impulses: ",self.count
            raise self.failureException
                


# creating a new test suite
FFT16Suite = unittest.TestSuite()
 
# adding a test case
FFT16Suite.addTest(unittest.makeSuite(TestDefaultFFT))
FFT16Suite.addTest(unittest.makeSuite(TestDefaultFFTImpulse0))
FFT16Suite.addTest(unittest.makeSuite(TestDefaultFFTImpulse1))
FFT16Suite.addTest(unittest.makeSuite(TestDefaultFFTImpulse2))
FFT16Suite.addTest(unittest.makeSuite(TestDefaultFFTImpulse3))
FFT16Suite.addTest(unittest.makeSuite(TestDefaultFFTImpulseRandom))
FFT16Suite.addTest(unittest.makeSuite(TestDefaultFFTRandom))
FFT16Suite.addTest(unittest.makeSuite(TestDefaultFFTZero))
if __name__ == '__main__':
    unittest.main()

