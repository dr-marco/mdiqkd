import netsquid as ns
from netsquid.nodes.node import Node
from netsquid.components.cchannel import ClassicalChannel
from netsquid.components.models import  FibreDelayModel
from netsquid.components.cqchannel import CombinedChannel
import mdi_node as mdi

# Config flag
fibreLen = 20 # length of the fiber channel
quantumLen = 20 # length of the quantum channel. This is used for both Alice and Bob
cSpeed=2*10**5 # speed of light of fiber channel
error_models = {"CDelayModel": FibreDelayModel(c=cSpeed)}
# Reset of the simulation
ns.sim_reset()
ns.set_random_state(seed=42)

# Declaration of the nodes
nodeA = Node("Alice",   port_names=["portCQ","portC_mdi","portC_out","portC_in"])
nodeB = Node("Bob"  ,   port_names=["portCQ","portC_mdi","portC_out","portC_in"])

mdi_node = Node("mdi", port_names=["portQ_1", "portC_1","portQ_2","portC_2"])

#Classical connection between Alice and Bob
CChannel_B_A = ClassicalChannel("CChannel_B->A",
                                delay=0,
                                length=fibreLen, 
                                models={"CDelayModel": FibreDelayModel(c=cSpeed)}) 
CChannel_A_B = ClassicalChannel("CChannel_A->B",
                                delay=0,
                                length=fibreLen, 
                                models={"CDelayModel": FibreDelayModel(c=cSpeed)})

nodeB.connect_to(nodeA, CChannel_B_A, local_port_name="portC_out", remote_port_name="portCA_in")
nodeA.connect_to(nodeB, CChannel_A_B, local_port_name="portC_out", remote_port_name="portCB_in")

#Classical connection between mdi node and client nodes
CChannel_mdi_A = ClassicalChannel("CChannel_mdi->A",
                                delay=0,
                                length=fibreLen, 
                                models={"CDelayModel": FibreDelayModel(c=cSpeed)}) 
CChannel_mdi_B = ClassicalChannel("CChannel_mdi->B",
                                delay=0,
                                length=fibreLen, 
                                models={"CDelayModel": FibreDelayModel(c=cSpeed)})

mdi_node.connect_to(nodeA, CChannel_mdi_A, local_port_name="portC_1", remote_port_name="portC_mdi")
mdi_node.connect_to(nodeB, CChannel_mdi_B, local_port_name="portC_2", remote_port_name="portC_mdi")

#Classical-Quantum connection from Alice and Bob to MDI node
CQChannel_A = CombinedChannel(name='QChannel_A_left',
                                   length=quantumLen,
                                   models=error_models
                                   )

CQChannel_B = CombinedChannel(name='QChannel_B_right',
                                   length=quantumLen,
                                   models=error_models
                                   )

nodeA.connect_to(mdi_node, CQChannel_A, local_port_name="portCQ", remote_port_name="portQ_1")
nodeB.connect_to(mdi_node, CQChannel_B, local_port_name="portCQ", remote_port_name="portQ_2")

# Measurement device independent protocol
mdi_protocol = mdi.mdiProtocol(mdi_node)

# start the mdi protocol
mdi_protocol.start()


# execute the protocol TODO uncomment the next line if you want to run the protocol
#stats = ns.sum_run(500000000) # high magic number to define a large amount of time to execute the QKD protocol

print("EOF")