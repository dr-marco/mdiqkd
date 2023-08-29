import netsquid as ns
from netsquid.protocols import NodeProtocol
import mdi_utils

# swithc node for star network architecture. Forwarding any message from sender to receiver

class switchProtocol(NodeProtocol):
    
    def __init__(self, node, client_nodes, rx_port_names, tx_port_names):
        super().__init__(node)
        self.node = node
        self.client_nodes = client_nodes # list of node connected to the network
        self.portNamesRx=rx_port_names # classic channel for receiving
        self.portNamesTx=tx_port_names # classic channel for transmission
        self.num_nodes = len(self.client_nodes) #number of nodes connected to the network


    def run(self):
        left_port = self.node.ports[self.portNameQ1]
        right_port = self.node.ports[self.portNameQ2]
        output_port_a = self.node.ports[self.portNameC1]
        output_port_b = self.node.ports[self.portNameC2]
        left_busy = False #Check the status of the left port, true if a qubit arrives
        right_busy = False #Check the status of the right port, true if a qubit arrives
        while True:
            #TODO implement expr generator function
            # wait for a qubit in one of the two ports                                                  head | tail
            status = yield (expr)  # (A | (B | (C | (D | (E)))))
            # check if is arrived on the left and then check if the second almost arrives instantly 
            i = 0
            while !(status.first_term.value):
                status = status.second_term.value
                i+=1
            rx_port = self.node.ports[self.portNamesRx[i]]
            message = rx_port.rx_input().items
            
            #TODO complete the switch class



            #     left_qubit_message,  = left_port.rx_input().items
            #     left_qubit = mdi_utils.extract_qubit(left_qubit_message)
            #     left_busy = True
            #     if (left_qubit != None):
            #         print("[-] photon received from alice at time " + str(ns.sim_time()))
            #     inner_status = yield (self.await_timer(mdiProtocol.max_delay_for_HOM_interference)) | (self.await_port_input(right_port))
            #     if inner_status.second_term.value:
            #         right_qubit_message, = right_port.rx_input().items
            #         right_qubit = mdi_utils.extract_qubit(right_qubit_message)
            #         right_busy = True
            # # check if is arrived on the right instead and then check if the left one almost arrives instantly
            # elif status.second_term.value:
            #     right_qubit_message, = right_port.rx_input().items
            #     right_qubit = mdi_utils.extract_qubit(right_qubit_message)
            #     right_busy = True
            #     if (right_qubit != None):
            #         print("[-] photon received from bob at time " + str(ns.sim_time()))
            #     inner_status = yield  (self.await_port_input(left_port)) | (self.await_timer(mdiProtocol.max_delay_for_HOM_interference))
            #     if inner_status.first_term.value:
            #         left_qubit_message,  = left_port.rx_input().items
            #         left_qubit = mdi_utils.extract_qubit(left_qubit_message)
            #         left_busy = True
            # # if both photons arrives almost in the same time, do the HOM interference and publish the MDI result publicly
            # if left_busy and right_busy:
            #     if (left_qubit != None) and (right_qubit != None):
            #         print("[+] two photons interference in the mdi node at time " + str(ns.sim_time()))
            #         meas_result = mdi_utils.di_measurement(left_qubit,right_qubit)
            #         output_port_a.tx_output(meas_result)
            #         output_port_b.tx_output(meas_result)
            # # reset the two status flag
            # left_busy = False
            # right_busy = False
                