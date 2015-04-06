from myhdl import Signal, Simulation, delay, always_comb

def Mux(counter_pin):
    counter2=Signal(False)
    @always_comb
    def muxLogic():
        counter2.next=counter_pin

    return muxLogic

# ...it can be instantiated as follows
def top_mux(): 
    counter=Signal(False)   
    mux_1 = Mux(counter)




a=top_mux()
