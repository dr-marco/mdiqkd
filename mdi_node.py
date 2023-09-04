import netsquid as ns
from netsquid.protocols import NodeProtocol
import mdi_utils

# MDI node for mdi architecture

class mdiProtocol(NodeProtocol):
    # delay parameter used to identify if there is HOM interference, i.e. if 2 photons arrive at the same time in the MDI node
    max_delay_for_HOM_interference = 1

    def __init__(self, node, client_nodes, quantum_port_names, classic_port_names, max_delay_for_protocol_wait=100000000):
        super().__init__(node)
        self.node = node
        # self.portNameQ1=port_names[0] # quantum left arm for Alice
        # self.portNameC1=port_names[1] # classic public channel for Alice
        # self.portNameQ2=port_names[2] # quantum right arm for Bob
        # self.portNameC2=port_names[3] # classic public channel for Bob
        self.client_nodes = client_nodes # client dictionary {num_id: name}
        self.num_nodes = len(self.client_nodes)
        self.portNamesQ = quantum_port_names
        self.portNamesC = classic_port_names
        self.max_delay_for_protocol_wait=max_delay_for_protocol_wait

    def generate_await_expr(self):
        # preparing the await expression as list_port = ( port | list_port ) e.g. (A | (B | (C | (D | (E)))))
        # if num_nodes is not greater than zero it returns None
        if not (self.num_nodes > 1):
            return None
        else:
            i = self.num_nodes - 1
            expr = self.await_port_input(self.node.ports[self.portNamesQ[i]])
            while i > 0:
                i-=1
                expr = ( self.await_port_input(self.node.ports[self.portNamesQ[i]]) | expr )
            return expr

    # ========================== Protocol run ==========================

    def run(self):
        #check if number of client is greater than one, i.e. if it is possible to perform the protocol
        if not (self.num_nodes > 1):
            print("Network too small to perform MDI-QKD protocol")
            return None

        while True:

            # --------------------------- Wait phase ---------------------------

            #flag used for end the protocol if no more qubits arrive at mdi node
            protocol_running = False
            #wait for any client that want to start the mdi-qkd protocol
            status = yield (self.generate_await_expr())
            #check from which port the node received the init message
            input_port_node = 0
            while not (status.first_term.value):
                status = status.second_term
                input_port_node+=1
            rx_port = self.node.ports[self.portNamesQ[input_port_node]]
            message = rx_port.rx_input().items
            #understand which other node will perfom the protocol
            message = mdi_utils.extract_message(message)
            destination_node = message.meta["destination"]

            # --------------------------- Setup phase ---------------------------

            if destination_node in self.client_nodes:
                time_stamp = message.items[0]
                left_port = self.node.ports[self.portNamesQ[input_port_node]]
                output_port_left = self.node.ports[self.portNamesC[input_port_node]]
                output_port_left.tx_output("ACK")
                left_name = self.client_nodes[input_port_node]
                dest_index = self.client_nodes.index(destination_node)
                right_port = self.node.ports[self.portNamesQ[dest_index]]
                output_port_right = self.node.ports[self.portNamesC[dest_index]]
                right_name = destination_node
                protocol_running = True
                print("[*] Performing protocol with "+left_name+" and "+right_name)

            left_busy = False #Check the status of the left port, true if a qubit arrives
            right_busy = False #Check the status of the right port, true if a qubit arrives

            # --------------------------- Protocol execution ---------------------------

            while protocol_running:
                # wait for a qubit in one of the two ports
                status = yield ((self.await_port_input(left_port)) | (self.await_port_input(right_port))) | self.await_timer(self.max_delay_for_protocol_wait)
                #check if protocol timed out
                if status.second_term.value:
                    protocol_running = False
                    print("[*] Protocol timed out. Reset")
                else:
                    status = status.first_term
                    # check if is arrived on the left and then check if the second almost arrives instantly
                    if status.first_term.value:
                        left_qubit_message,  = left_port.rx_input().items
                        left_qubit = mdi_utils.extract_qubit(left_qubit_message)
                        left_busy = True
                        if (left_qubit != None):
                            print("[-] photon received from " + left_name + " at time " + str(ns.sim_time()))
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
                            print("[-] photon received from "+ right_name +" at time " + str(ns.sim_time()))
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
                            output_port_left.tx_output(meas_result)
                            output_port_right.tx_output(meas_result)
                    # reset the two status flag
                    left_busy = False
                    right_busy = False
