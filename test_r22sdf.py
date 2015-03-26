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
        """Verifica la funcionalidad de una butterfly r2^2 serial como una FFT4"""
        t=test(clock,reset,a,d)
        sim=Simulation(t,clkgen)
        for i in range(30):
            sim.run(1,quiet=1)
            print i,clock,reset,a,d
 
if __name__ == '__main__':
    unittest.main() # llamarlo de la linea de comandos ejecuta todas las pruebas
    
