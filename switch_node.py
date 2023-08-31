import netsquid as ns
from netsquid.protocols import NodeProtocol
import mdi_utils

# switch node for star network architecture. Forwarding any message from sender to destination

class switchProtocol(NodeProtocol):
    
    def __init__(self, node, client_nodes, rx_port_names, tx_port_names):
        super().__init__(node)
        self.node = node
        self.client_nodes = client_nodes # list of node connected to the network
        self.portNamesRx=rx_port_names # classic channel for receiving
        self.portNamesTx=tx_port_names # classic channel for transmission
        self.num_nodes = len(self.client_nodes) #number of nodes connected to the network

    def generate_await_expr(self):
        # preparing the await expression as list_port = ( port | list_port ) e.g. (A | (B | (C | (D | (E)))))
        # if num_nodes is not greater than zero it returns None
        if !(self.num_nodes > 1):
            return None
        else:
            i = len(self.num_nodes) - 1
            expr = self.await_port_input(self.node.ports[self.portNamesRx[i]])
            while i > 0:
                i-=1
                expr = ( self.await_port_input(self.node.ports[self.portNamesRx[i]]) | expr )
            return expr

    def run(self):

        while True:

            # i = len(self.num_nodes) - 1
            # expr = self.await_port_input(self.node.ports[self.portNamesRx[i]])
            # while i > 0:
            #     i-=1
            #     expr = ( self.await_port_input(self.node.ports[self.portNamesRx[i]]) | expr )
            # wait for a message from any input port
            status = yield (generate_await_expr())
            # check from which input port the message is arrived
            input_port_node = 0
            while !(status.first_term.value):
                status = status.second_term.value
                input_port_node+=1
            rx_port = self.node.ports[self.portNamesRx[input_port_node]]
            message = rx_port.rx_input().items
            
            #TODO complete the switch class

