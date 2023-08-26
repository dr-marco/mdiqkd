import netsquid as ns
from netsquid.protocols import NodeProtocol
import client_utils

# new version of the client node, should work with sim_run.py

class clientProtocol(NodeProtocol):

    # delay of 4 milliseconds, parameter that could be tuned    
    delay_for_wait = 4000 

    def __init__(self, node, port_names, init=False):
        super().__init__(node)
        self.num_bits=num_bits
        self.node = node
        self.portNameQ1="portCQ"    #classical quantum communication channel to mdi node
        self.portNameC1="portC_mdi" #receive port from mdi
        self.portNameC2="portC_out" #to another classical node
        self.portNameC3="portC_in"  #from another classical node
        #self.HbasisList=Random_basis_gen(self.num_bits)  #TODO Random_basis_gen from function module to use
        #self.XbasisList=Random_basis_gen(self.num_bits)
        #self.loc_measRes=[]
        self.key=[]
        self.init=init #flag in order to say if the node is the initializer or not

        #TODO add a random number for the initialize event: when the clock value is equal to this number
        # then a handler start the init phase so the first node (suppose Alice node) can send the first message
        # and start the protocol. The first message will contain a timestamp that will be used as reference 
        # for sending to MDI node the two photons at the same time


    def run(self):
        quantum_port = self.node.ports[self.portNameQ1]
        result_port = self.node.ports[self.portNameC1] 
        output_port = self.node.ports[self.portNameC2]
        input_port = self.node.ports[self.portNameC3]
        
        if init:
            #start the protocol sending the first message to the other node
            yield self.await_timer(delay_for_wait**2) #TODO insert random time value
            time_start = ns.sim_time()
            output_port.tx_output(time_start)
        else: 
            #wait for init
            yield self.await_port_input(input_port)
            time_start, = input_port.rx_input().items

        # for numero di bit da negoziare
        #     do at timestamp_init + delta_time * num_current_step
        #         send qubit and wait result
        #         save result in array

        if init:
            # publish basis chosen and wait other part's basis
        else: 
            # wait other part's basis chosen and publish chosen basis

        # compare the basis 
        # generate the correct key, if necessary do flip bit in bob's case (if-else init)

        init = false
        return null 