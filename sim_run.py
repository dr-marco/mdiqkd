import netsquid as ns
from netsquid.nodes.node import Node
import mdi_node as mdi

# Config flag
fibreLen = 20 # length of the fiber channel
quantumLen = 20 # length of the quantum channel. This is used for both Alice and Bob
# Reset of the simulation
ns.sim_reset()
ns.set_random_state(seed=42)

# Declaration of the nodes
nodeA = Node("Alice",   port_names=["portQA_1","portQA_2","portCA_1","portCA_2","portCA_3"])
nodeB = Node("Bob"  ,   port_names=["portQB_1","portQB_2","portCB_1","portCB_2","portCB_3"])
#nodeC = Node("Charlie", port_names=["portQC_1","portQC_2","portCC_1","portCC_2"])
#nodeD = Node("Dave"  ,  port_names=["portQD_1","portQD_2","portCD_1","portCD_2"])

mdi_node = Node("mdi", port_names=["portQ_1","portQ_2","portC_1"])

#Classical connection between Alice and Bob
CChannel_B_A = ClassicalChannel("CChannel_B->A",
                                delay=0,
                                length=fibreLen, 
                                models={"CDelayModel": FibreDelayModel(c=cSpeed)}) #TODO define fibreLen
CChannel_A_B = ClassicalChannel("CChannel_A->B",
                                delay=0,
                                length=fibreLen, 
                                models={"CDelayModel": FibreDelayModel(c=cSpeed)})

nodeB.connect_to(nodeA, CChannel_B_A, local_port_name="portCB_2", remote_port_name="portCA_3")
nodeA.connect_to(nodeB, CChannel_A_B, local_port_name="portCA_2", remote_port_name="portCB_3")

#nodeA.connect_to(nodeB, MyCChannel2, local_port_name="portCA_1", remote_port_name="portCB_2")

#Quantum connection from Alice and Bob to MDI node. Left and right channel to connect both left and right port to the MDI node
# Be careful with this implementation
QChannel_A_left = QuantumChannel(name='QChannel_A_left',
                                   length=quantumLen,
                                   models=error_models
                                   )

QChannel_A_right = QuantumChannel(name='QChannel_A_right',
                                   length=quantumLen,
                                   models=error_models
                                   )

QChannel_B_left = QuantumChannel(name='QChannel_B_left',
                                   length=quantumLen,
                                   models=error_models
                                   )

QChannel_B_right = QuantumChannel(name='QChannel_B_right',
                                   length=quantumLen,
                                   models=error_models
                                   )

nodeA.connect_to(mdi_node, QChannel_A_left, local_port_name="portQA_1", remote_port_name="portQ_1")
nodeA.connect_to(mdi_node, QChannel_A_right, local_port_name="portQA_2", remote_port_name="portQ_2")
nodeB.connect_to(mdi_node, QChannel_B_left, local_port_name="portQB_1", remote_port_name="portQ_1")
nodeB.connect_to(mdi_node, QChannel_B_right, local_port_name="portQB_2", remote_port_name="portQ_1")

# Measurement device independent protocol
mdi_protocol = mdi.mdi_node(mdi_node)

# start the mdi protocol
mdi_protocol.start()


# execute the protocol TODO uncomment the next line if you want to run the protocol
#stats = ns.sum_run(500000000) # high magic number to define a large amount of time to execute the QKD protocol