import myhdl
from myhdl import *
from math import *
from numpy import *
from r22sdf import *
import unittest
from random import *
from test_r22sdf import gen_bitreverse
N_LOG2    = 8
N=2**N_LOG2
TF_WDTH   = 10
DIN_WDTH  = 8
META_WDTH = 1
DOUT_WDTH = 16

def gen_check(stim):
    fft_reference = (fft.fft( [ complex(i[0],i[1]) for i in stim] ) )
    fft_reference_r = [ fft_reference[i] for i in gen_bitreverse(int(log(N)/log(2)))]
    out_re=tuple([ int ( real(i).round()) for i in fft_reference_r])
    out_im=tuple([ int ( imag(i).round()) for i in fft_reference_r])
    return out_re,out_im

impulse = (2**DIN_WDTH-1)/2
zero = 0
stim = [[impulse]*2 if i in range(16) else [zero]*2 for i in range(2**N_LOG2) ]
stim_re = tuple([i[0] for i in stim])
stim_im = tuple([i[1] for i in stim])
t_check_re,t_check_im = gen_check(stim)



def tb():
    
    clk = Signal(bool(0))
    rst_n = Signal(bool(0))
    din_meta = Signal(intbv(0)[META_WDTH:])
    din_re = Signal(intbv(0)[ DIN_WDTH:])
    din_im = Signal(intbv(0)[ DIN_WDTH:])
    din_nd = Signal(bool(1))
    dout_meta = Signal(intbv(0)[META_WDTH:])
    dout_re = Signal(intbv(0)[DOUT_WDTH:])
    dout_im = Signal(intbv(0)[DOUT_WDTH:])
    check_re = Signal(intbv(0)[DOUT_WDTH:])
    check_im = Signal(intbv(0)[DOUT_WDTH:])
    dout_nd = Signal(bool(1))
    stim_counter = Signal(modbv(0,0,N)) 
    
    @instance
    def tbclk():
        clk.next = False
        while True:
            yield delay(3)
            clk.next = not clk
        
    @instance
    def stimulus():        
        rst_n.next = False
        for i in range(2**N_LOG2):
            yield delay(1)
        yield clk.posedge
        rst_n.next=True

    @always(clk.posedge)
    def stim():
        if (rst_n==True):
            stim_counter.next = stim_counter+1
            stim_counter_aux = stim_counter+N-1
            din_re.next[:] = stim_re[stim_counter]
            din_im.next[:] = stim_im[stim_counter]
            check_re.next[:] = t_check_re[stim_counter]
            check_im.next[:] = t_check_im[stim_counter]
        else:
            stim_counter.next=0
            
    return instances()



toVerilog(tb)

