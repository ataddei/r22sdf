from myhdl import *
from math import *


def Butterfly (i_data_a,i_data_b,o_data_a,o_data_b):
    @always_comb
    def bf():
        o_data_a.next=i_data_a+i_data_b
        o_data_b.next=i_data_a-i_data_b
    return bf

def Butterfly21 (i_control_s,i_data_aa,i_data_bb,o_data_aa,o_data_bb):
    selfc=Signal(complex(0,0))
    selfd=Signal(complex(0,0))
    u_bf=Butterfly(i_data_aa,i_data_bb,selfc,selfd)       
    @always_comb
    def bf21():
        
        if i_control_s:
        
            o_data_aa.next=selfd
            o_data_bb.next=selfc
            
        else:
            o_data_aa.next=i_data_bb
            o_data_bb.next=i_data_aa
            
    return instances()

def Butterfly22 (i_control_t,i_control_s,i_data_aa,i_data_bb,o_data_aa,o_data_bb):
    selfa=Signal(complex(0,0))
    selfb=Signal(complex(0,0))
    selfc=Signal(complex(0,0))
    selfd=Signal(complex(0,0))
    
    u_bf=Butterfly(selfa,selfb,selfc,selfd)       
    @always_comb
    def bf22():
        if i_control_s==False:
            selfa.next=i_data_aa
            selfb.next=i_data_bb
            o_data_aa.next=i_data_bb
            o_data_bb.next=i_data_aa
        else:
            selfa.next=i_data_aa
            if i_control_t:
                selfb.next=i_data_bb
            else:
                selfb.next=i_data_bb*complex(0,-1)
            o_data_aa.next=selfd
            o_data_bb.next=selfc
       
    return instances()


def stage(i_data,reset,clock,o_data,N=1):
    fifo1=[Signal(complex(0,0)) for ii in range(N*2)]
    fifo2=[Signal(complex(0,0)) for ii in range(N)]
    a=Signal(complex(0,0))
    b=Signal(complex(0,0))
    c=Signal(complex(0,0))
    d=Signal(complex(0,0))
    control_s=Signal(False)
    control_t=Signal(False)
    counter=Signal(modbv(0,0,2**(N*2)))
    u_bf21=Butterfly21(control_s,fifo1[len(fifo1)-1],i_data,a,b)
    u_bf22=Butterfly22(control_s,control_t,fifo2[len(fifo2)-1],b,c,o_data)
    @always (clock.posedge,reset)
    def counterandfifos():
        
        if reset==True:
            counter.next=0
        else:
            counter.next=counter+1
        
        
            #print b,o_data,control_t,control_s
            for i in range(len(fifo1)):
                fifo1[i].next = a if i==0 else fifo1[i-1]
        
            for i in range(len(fifo2)):
                fifo2[i].next = c if i==0 else fifo2[i-1]
        
    @always_comb
    def control():
        control_s.next=counter[1]
        control_t.next=counter[0]
    
    return instances()

