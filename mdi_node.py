import netsquid as ns
from netsquid.protocols import NodeProtocol
import mdi_utils

class mdiProtocol(NodeProtocol):
    def __init__(self, node, status=0):
        super().__init__()
        self.num_bits=num_bits
        self.node = node
        self.status = status
        self.portNameQ1=port_names[0] #left arm
        self.portNameQ2=port_names[1] #right arm
        self.portNameC1=port_names[2]  #to
        self.loc_measRes=[]
        self.key=[]
        self.sourceQList=[]


    def run():
        left_port = self.node.portNameQ1
        right_port = self.node.portNameQ2
        left_busy = False
        right_busy = False
        while True:
            status = yield (self.await_port_input(left_port)) | (self.await_port_input(right_port))
            if status.first_term.value:
                left_qubit,  = left_port.rx_input().items
                left_busy = True
            if status.second_term.value:
                right_qubit, = right_port.rx_input().items
                right_busy = True
            if left_busy and right_busy:
                #do stuff
                di_measurement(left_qubit,right_qubit)
                left_busy = False
                right_busy = False
                