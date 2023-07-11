import netsquid as ns
from netsquid.nodes.node import Node

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

nodeA.connect_to(nodeB, MyCChannel2, local_port_name="portCA_1", remote_port_name="portCB_2")