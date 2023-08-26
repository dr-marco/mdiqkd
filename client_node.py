import netsquid as ns
from netsquid.protocols import NodeProtocol
import client_utils

# new version of the client node, should work with sim_run.py

class clientProtocol(NodeProtocol):

    # delay of 4 milliseconds, parameter that could be tuned    
    delay_for_wait = 4000 
    # flag to identify if the particular node client is the first to perform the protocol or not. Default set to false
    initializer = false 

    def __init__(self, node, port_names):
        super().__init__()
        self.num_bits=num_bits
        self.node = node
        self.portNameQ1="portCQ"    #classical quantum communication channel to mdi node
        self.portNameC1="portC_mdi" #receive port from mdi
        self.portNameC2="portC_out" #to another classical node
        self.portNameC2="portC_in"  #from another classical node
        #self.HbasisList=Random_basis_gen(self.num_bits)  #TODO Random_basis_gen from function module to use
        #self.XbasisList=Random_basis_gen(self.num_bits)
        #self.loc_measRes=[]
        self.key=[]

        #TODO add a random number for the initialize event: when the clock value is equal to this number
        # then a handler start the init phase so the first node (suppose Alice node) can send the first message
        # and start the protocol. The first message will contain a timestamp that will be used as reference 
        # for sending to MDI node the two photons at the same time
        
    def start(self):
        start_protocol()

    def start_protocol(): # TODO modify this implementation, run function first to call
        #do stuff for initialize protocol

        this.run(init=True)
        return null


    def run(init=False):
        port = self.node.ports[self.portNameQ2] #use right arm as default
        input_port = self.node.ports[self.portNameC1]
        output_port = self.node.ports[self.portNameC2]
        
        if init:
            port = self.node.ports[self.portNameQ1]
            time_start = ns.sim_time()
            #start the protocol sending the first message to the other node
        else: 
            #wait for init

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