import netsquid as ns
from netsquid.protocols import NodeProtocol
from netsquid.components.component import Message as msg
import client_utils as c_utils

# new version of the client node, should work with sim_run.py

class clientProtocol(NodeProtocol):

    ver_ratio = 0.25 #ratio to split the key generated in the actual key and in the verification key for the validation phase

    def __init__(self, node, num_bits=64, init=False,
                    delay_for_wait = 250000, delay_for_first = 1000000, delta_delay = 500,
                    port_names=["portCQ","portC_mdi","portC_out","portC_in"], other_nodes=[]):
        super().__init__(node)
        self.num_bits=num_bits
        self.node = node
        self.portNameQ1=port_names[0] #classical quantum communication channel to mdi node
        self.portNameC1=port_names[1] #receive port from mdi
        self.portNameC2=port_names[2] #to another classical node
        self.portNameC3=port_names[3] #from another classical node
        self.HbasisList=c_utils.random_basis_gen(self.num_bits) # array of basis randomly chosen
        self.XbasisList=c_utils.random_basis_gen(self.num_bits) # array of bits randomly chosen
        self.loc_measRes=[None] * self.num_bits # array for storing the mdi result
        self.key=[] # empty key # TODO add a dictionary to save more than one key with multiple nodes
        self.init=init #flag in order to say if the node is the initializer or not
        self.late_init = False #flag used if an init node receive a start message before sending his first. Simply standby the protocol for this init node
        self.delay_for_first = delay_for_first
        self.delay_for_wait = delay_for_wait
        self.delta_delay = delta_delay
        self.other_nodes = other_nodes


    def run(self):
        delay_for_first = self.delay_for_first
        delay_for_wait = self.delay_for_wait
        delta_delay = self.delta_delay
        quantum_port = self.node.ports[self.portNameQ1]
        result_port = self.node.ports[self.portNameC1] 
        output_port = self.node.ports[self.portNameC2]
        input_port = self.node.ports[self.portNameC3]
        
        while True:
            if self.init:
                #start the protocol sending the first message to the other node
                expr = (self.await_timer(c_utils.random_start_time(start=ns.sim_time()))) | (self.await_port_input(input_port))
                start = yield (expr) # edge case two init nodes. Yield should listen also the input port for others init messages even if the node is in init=True
                time_start = ns.sim_time()
                if start.second_term.value:
                    self.init = False
                    self.late_init = True
                    time_start, = input_port.rx_input().items
                else:
                    output_port.tx_output(msg(time_start, sender=self.node.name, destination=self.other_nodes[0])) #TODO init to mdi node
            else: 
                #wait for init
                yield self.await_port_input(input_port)
                time_start, = input_port.rx_input().items

            print(self.node.name + " start time: " + str(time_start))
            time_first_qubit = time_start + delay_for_first
            for i in range(self.num_bits):
                # prepare the qubit photon
                qubit=c_utils.generate_quantum_photon(self.XbasisList[i], self.HbasisList[i])
                yield self.await_timer(end_time=time_first_qubit+i*delay_for_wait)
                print(self.node.name + " time: " + str(time_first_qubit+i*delay_for_wait))
                # send the qubit to the mdi_node
                quantum_port.tx_output({None,qubit}) #message format for CombinedChannel -> {classical, quantum}

                # wait for mdi results
                mdi_result = yield (self.await_port_input(result_port)) | (self.await_timer(delay_for_wait-delta_delay))
                if mdi_result.first_term.value:
                    # save the result if the mdi_node detect the photons
                    mdi_meas, = result_port.rx_input().items
                    self.loc_measRes[i] = mdi_meas

            # publish basis chosen and wait other part's basis
            output_port.tx_output(msg(self.HbasisList, sender=self.node.name, destination=self.other_nodes[0]))
            yield self.await_port_input(input_port)
            other_client_basis = input_port.rx_input().items

            # compare the basis and generate the correct key, if necessary do flip bit in bob's case
            temp_key = []
            for i in range(self.num_bits):
                if self.HbasisList[i] == other_client_basis[i]:
                    if self.loc_measRes[i] != None:
                        i_result = c_utils.measurement_result_eval(self.init, self.HbasisList[i], self.XbasisList[i], self.loc_measRes[i])
                        if i_result != None:
                            temp_key.append(i_result)

            # publish portion of the key and wait other part's key
            if len(temp_key) >= (1/clientProtocol.ver_ratio):
                # splitting the temp_key in:
                #   verification_key used for the validation phase
                verification_key = temp_key[:int(len(temp_key)*clientProtocol.ver_ratio)]
                #   generated_key saved if the validation is successfull
                generated_key = temp_key[int(len(temp_key)*clientProtocol.ver_ratio):]
                output_port.tx_output(msg(verification_key, sender=self.node.name, destination=self.other_nodes[0]))
                yield self.await_port_input(input_port)
                message = input_port.rx_input()
                other_client_ver_key = message.items #.meta["sender"]

                if verification_key == other_client_ver_key:
                    self.key = generated_key
                    print(self.node.name + " generated key successfully: \t" + "".join([str(j) for j in self.key]))
                else:
                    print("[!] MDI-QKD protocol failed. The two validation key arrays are not equal")
            else:
                print(self.node.name + " generated key is too short for validation: :\t" + "".join([str(j) for j in temp_key]))

            # flag reset
            self.init = False
            if self.late_init:
                self.late_init = False
                self.init = True