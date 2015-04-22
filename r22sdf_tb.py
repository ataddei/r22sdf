import myhdl
from myhdl import *
from math import *
from numpy import *
from r22sdf import *
import unittest
from random import *
N_LOG2    = 8
N=2**N_LOG2
TF_WDTH   = 8
DIN_WDTH  = 8
META_WDTH = 1
DOUT_WDTH = 11 

impulse=(2**DIN_WDTH-1)
zero=0
stim=[ [impulse]*2 if i==0 else [zero]*2 for i in range(2**N_LOG2) ]
stim_re=tuple([i[0] for i in stim])
stim_im=tuple([i[1] for i in stim])
def tb():
    
   
    clk=Signal(bool(0))
    rst_n=Signal(bool(0))
    din_meta=Signal(intbv(0)[META_WDTH:])
    din_re=Signal(intbv(0)[ DIN_WDTH:])
    din_im=Signal(intbv(0)[ DIN_WDTH:])
    din_nd=Signal(bool(1))
    dout_meta=Signal(intbv(0)[META_WDTH:])
    dout_re=Signal(intbv(0)[DOUT_WDTH:])
    dout_im=Signal(intbv(0)[DOUT_WDTH:])
    dout_nd=Signal(bool(1))
    stim_counter=Signal(modbv(0,0,N))
    
     
    @instance
    def clkgen():
        while True:
            clk.next = not clk
            yield delay(1)
    @instance
    def stimulus():
        rst_n.next = False
        for i in range(2**N_LOG2):
            yield delay(1)
        yield delay(1)
        rst_n.next=True
        while True:                        
            yield delay(1)
    @always(clk.posedge)
    def stim():
        if (rst_n==True):
            stim_counter.next=stim_counter+1
            din_re.next[:]=stim_re[stim_counter]
            din_im.next[:]=stim_im[stim_counter]
            print din_re,din_im
    return instances()

toVerilog(tb)
