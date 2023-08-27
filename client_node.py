import netsquid as ns
from netsquid.protocols import NodeProtocol
import client_utils as cu

# new version of the client node, should work with sim_run.py

class clientProtocol(NodeProtocol):

    # delay of 4 milliseconds, parameter that could be tuned    
    delay_for_wait = 250000 
    delay_for_first = 1000000

    def __init__(self, node, num_bits=64, init=False): # port_names, # parameter moved out
        super().__init__(node)
        self.num_bits=num_bits
        self.node = node
        self.portNameQ1="portCQ"    #classical quantum communication channel to mdi node
        self.portNameC1="portC_mdi" #receive port from mdi
        self.portNameC2="portC_out" #to another classical node
        self.portNameC3="portC_in"  #from another classical node
        self.HbasisList=cu.random_basis_gen(self.num_bits)  
        self.XbasisList=cu.random_basis_gen(self.num_bits)
        self.loc_measRes=[None] * self.num_bits
        self.key=[]
        self.init=init #flag in order to say if the node is the initializer or not

        #TODO add a random number for the initialize event: when the clock value is equal to this number
        # then a handler start the init phase so the first node (suppose Alice node) can send the first message
        # and start the protocol. The first message will contain a timestamp that will be used as reference 
        # for sending to MDI node the two photons at the same time


    def run(self):
        delay_for_first = clientProtocol.delay_for_first
        delay_for_wait = clientProtocol.delay_for_wait
        quantum_port = self.node.ports[self.portNameQ1]
        result_port = self.node.ports[self.portNameC1] 
        output_port = self.node.ports[self.portNameC2]
        input_port = self.node.ports[self.portNameC3]
        
        while True:
            if self.init:
                #start the protocol sending the first message to the other node
                yield self.await_timer(12000000) #TODO insert random time value
                time_start = ns.sim_time()
                output_port.tx_output(time_start)
            else: 
                #wait for init
                yield self.await_port_input(input_port)
                time_start, = input_port.rx_input().items

            print(self.node.name + " time: " + str(time_start))
            time_first_qubit = time_start + delay_for_first
            for i in range(self.num_bits):
                # prepare the qubit photon
                qubits = ns.qubits.create_qubits(1)
                qubit = qubits[0]
                if self.XbasisList[i]%2==1: 
                    ns.qubits.operate(qubit, ns.X)
                if self.HbasisList[i]%2==1: 
                    ns.qubits.operate(qubit, ns.H)
                yield self.await_timer(end_time=time_first_qubit+i*delay_for_wait)
                print(self.node.name + " time: " + str(time_first_qubit+i*delay_for_wait))
                # send the qubit to the mdi_node
                quantum_port.tx_output(qubit)
                # wait for mdi results
                mdi_result = yield (self.await_port_input(result_port)) | (self.await_timer(delay_for_wait-500)) # define minus 500 as parameter
                if mdi_result.first_term.value:
                    # save the result if the mdi_node detect the photons
                    mdi_meas, = result_port.rx_input().items
                    self.loc_measRes[i] = mdi_meas

            # publish basis chosen and wait other part's basis
            output_port.tx_output(self.HbasisList)
            yield self.await_port_input(input_port)
            other_client_basis = input_port.rx_input().items

            # compare the basis and generate the correct key, if necessary do flip bit in bob's case
            for i in range(self.num_bits):
                if self.HbasisList[i] == other_client_basis[i]:
                    if self.loc_measRes[i] != None:
                        i_result = cu.measurement_result_eval(self.init, self.HbasisList[i], self.XbasisList[i], self.loc_measRes[i])
                        if i_result != None:
                            self.key.append(i_result)

            self.init = False
            print(self.node.name + " generated key: " + str(self.key)) 