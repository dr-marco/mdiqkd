import netsquid as ns
from netsquid.protocols import NodeProtocol
import mdi_utils

# MDI node for thin mdi architecture. Not very usable for more than two clients

class mdiProtocol(NodeProtocol):
    # delay parameter used to identify if there is HOM interference, i.e. if 2 photons arrive at the same time in the MDI node
    max_delay_for_HOM_interference = 1 

    def __init__(self, node, status=0):
        super().__init__()
        self.node = node
        self.portNameQ1=port_names[0] #quantum left arm
        self.portNameQ2=port_names[1] #quantum right arm
        self.portNameC1=port_names[2] #classic public channel


    def run():
        left_port = self.node.ports[self.portNameQ1]
        right_port = self.node.ports[self.portNameQ2]
        output_port = self.node.ports[self.portNameC1]
        left_busy = False #Check the status of the left port, true if a qubit arrives
        right_busy = False #Check the status of the right port, true if a qubit arrives
        while True:
            # wait for a qubit in one of the two ports
            status = yield (self.await_port_input(left_port)) | (self.await_port_input(right_port)) 
            # check if is arrived on the left and then check if the second almost arrives instantly
            if status.first_term.value:
                left_qubit,  = left_port.rx_input().items
                left_busy = True
                yield (self.await_timer(max_delay_for_HOM_interference)) | (self.await_port_input(right_port))
                if status.second_term.value:
                    right_qubit, = right_port.rx_input().items
                    right_busy = True
            # check if is arrived on the right instead and then check if the left one almost arrives instantly
            elif status.second_term.value:
                right_qubit, = right_port.rx_input().items
                right_busy = True
                yield self.await_timer(max_delay_for_HOM_interference) | (self.await_port_input(left_port))
                if status.first_term.value:
                    left_qubit,  = left_port.rx_input().items
                    left_busy = True
            # if both photons arrives almost in the same time, do the HOM interference and publish the MDI result publicly
            if left_busy and right_busy:
                meas_result = di_measurement(left_qubit,right_qubit)
                output_port.tx_output(meas_result)
            # reset the two status flag
            left_busy = False
            right_busy = False
                