from myhdl import *
from math import *
from  numpy import *

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


def stage(i_data,reset,clock,o_data,counter_pin,index,N=1,FFT=16):
    fifo1=[Signal(complex(0,0)) for ii in range(N*(2**N))]
    fifo2=[Signal(complex(0,0)) for ii in range(N*(2**(N-1)))]
    a=Signal(complex(0,0))
    b=Signal(complex(0,0))
    c=Signal(complex(0,0))
    d=Signal(complex(0,0))
    counter_s=Signal(False)
    counter_t=Signal(False)
    #counter_tw=Signal(modbv(0,0,FFT))
    @always_comb
    def control_muxes():
        counter_s.next=counter_pin(2*(N-1)+1)
        counter_t.next=counter_pin(2*(N-1))
       
    u_bf22=Butterfly22(counter_s,counter_t,fifo2[len(fifo2)-1],b,c,d)
    u_bf21=Butterfly21(counter_s,fifo1[len(fifo1)-1],i_data,a,b)
    
    @always (clock.posedge,reset)
    def fifos():
         if reset==False:
            #print b,o_data,control_t,control_s
            
            for i in range(len(fifo1)):
                fifo1[i].next = a if i==0 else fifo1[i-1]
        
            for i in range(len(fifo2)):
                fifo2[i].next = c if i==0 else fifo2[i-1]
             
    @always_comb
    def out_twiddle():
        
        counter_tw=mod(counter_pin+4,FFT)
        if (N!=1):
            o_data.next=d*conj(e**(complex(0,-2*pi*index[counter_tw]/(1.0*FFT))))

        else:
            o_data.next=d
    @always (clock.negedge)
    def print_values():
        if (N!=1):
            counter_tw=mod(counter_pin+4,FFT)
            print N,counter_pin,counter_s,counter_t,i_data,b,d,index[counter_tw],'counter_tw: ',counter_tw
    return instances()


def r22sdf_top(i_data,reset,clock,o_data,N=1):
    FFT=2**(2*N)
    counter=Signal(modbv(0,0,2**(N*2)))
    stage_data_in_wire=[Signal(complex(0,0)) for ii in range(N)]
    stage_data_out_wire=[Signal(complex(0,0)) for ii in range(N)]
    butterflies=[None for i in range(N)]
    index=twiddle_calc(2**(2*N))
    
    @always(clock.posedge,reset)
    def counter_seq():
        if reset==True:
            counter.next=0
        else:
            counter.next=counter+1
            #print counter,stage_data_in_wire[0],stage_data_out_wire[0]
    for i in range(N):
        if i==0:
            stage_data_in_wire[i]=i_data
        else:
            stage_data_in_wire[i]=stage_data_out_wire[i-1]
        if i==(N-1):
            stage_data_out_wire[i]=o_data
            butterflies[i]=stage(stage_data_in_wire[i],reset,clock,stage_data_out_wire[i],counter,[0]*FFT,1,FFT)
        else:butterflies[i]=stage(stage_data_in_wire[i],reset,clock,stage_data_out_wire[i],counter,index[i],N-i,FFT)
        
    return instances()
        
        

def twiddle_calc(N=16):
    k=range(int(ceil((log2(N)/log2(4)))-1))
    a=[range(N/2**(2*i)) for i in k]
    t=[]
    for j in k:
        m=(N/2**(2+2*j))
        p=[]
        p=p+([0 for i in range(m)])
        p=p+([2*(2**(2*j))*(i-m) for i in range(m,2*m)])
        p=p+([(2**(2*j))*(i-2*m) for i in range(2*m,3*m)])
        p=p+([(3*2**(2*j))*(i-3*m) for i in range(3*m,4*m)])
        if j>0:
            t.append(p*(j*4))
        else:
            t.append(p)
    
    return t if k else [0]*N

p=twiddle_calc(16)
