import netsquid as ns
from netsquid.protocols import NodeProtocol
import mdi_utils

# MDI node for thick mdi architecture
# TODO early implementation for only Alice and Bob! To modify in order to increase the number of clients

class mdiProtocol(NodeProtocol):
    # delay parameter used to identify if there is HOM interference, i.e. if 2 photons arrive at the same time in the MDI node
    max_delay_for_HOM_interference = 1

    def __init__(self, node, port_names=["portQ_1", "portC_1","portQ_2","portC_2"]):
        super().__init__(node)
        self.node = node
        self.portNameQ1=port_names[0] # quantum left arm for Alice
        self.portNameC1=port_names[1] # classic public channel for Alice
        self.portNameQ2=port_names[2] # quantum right arm for Bob
        self.portNameC2=port_names[3] # classic public channel for Bob


    def run(self):
        left_port = self.node.ports[self.portNameQ1]
        right_port = self.node.ports[self.portNameQ2]
        output_port_a = self.node.ports[self.portNameC1]
        output_port_b = self.node.ports[self.portNameC2]
        left_busy = False #Check the status of the left port, true if a qubit arrives
        right_busy = False #Check the status of the right port, true if a qubit arrives
        while True:
            # wait for a qubit in one of the two ports                                                  head | tail
            status = yield (self.await_port_input(left_port)) | (self.await_port_input(right_port))  # (A | (B | (C | (D | (E)))))
            # check if is arrived on the left and then check if the second almost arrives instantly 
            if status.first_term.value:
                left_qubit_message,  = left_port.rx_input().items
                left_qubit = mdi_utils.extract_qubit(left_qubit_message)
                left_busy = True
                if (left_qubit != None):
                    print("[-] photon received from alice at time " + str(ns.sim_time()))
                inner_status = yield (self.await_timer(mdiProtocol.max_delay_for_HOM_interference)) | (self.await_port_input(right_port))
                if inner_status.second_term.value:
                    right_qubit_message, = right_port.rx_input().items
                    right_qubit = mdi_utils.extract_qubit(right_qubit_message)
                    right_busy = True
            # check if is arrived on the right instead and then check if the left one almost arrives instantly
            elif status.second_term.value:
                right_qubit_message, = right_port.rx_input().items
                right_qubit = mdi_utils.extract_qubit(right_qubit_message)
                right_busy = True
                if (right_qubit != None):
                    print("[-] photon received from bob at time " + str(ns.sim_time()))
                inner_status = yield  (self.await_port_input(left_port)) | (self.await_timer(mdiProtocol.max_delay_for_HOM_interference))
                if inner_status.first_term.value:
                    left_qubit_message,  = left_port.rx_input().items
                    left_qubit = mdi_utils.extract_qubit(left_qubit_message)
                    left_busy = True
            # if both photons arrives almost in the same time, do the HOM interference and publish the MDI result publicly
            if left_busy and right_busy:
                if (left_qubit != None) and (right_qubit != None):
                    print("[+] two photons interference in the mdi node at time " + str(ns.sim_time()))
                    meas_result = mdi_utils.di_measurement(left_qubit,right_qubit)
                    output_port_a.tx_output(meas_result)
                    output_port_b.tx_output(meas_result)
            # reset the two status flag
            left_busy = False
            right_busy = False
                