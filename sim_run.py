import netsquid as ns
from netsquid.nodes.node import Node

nodeA = Node("Alice",   port_names=["portQA_1","portQA_2","portCA_1","portCA_2"])
nodeB = Node("Bob"  ,   port_names=["portQB_1","portQB_2","portCB_1","portCB_2"])
#nodeC = Node("Charlie", port_names=["portQC_1","portQC_2","portCC_1","portCC_2"])
#nodeD = Node("Dave"  ,  port_names=["portQD_1","portQD_2","portCD_1","portCD_2"])

mdi_node = Node("mdi", port_names=["portQ_1","portQ_2","portC_1"])

MyCChannel = ClassicalChannel("CChannel_B->A",delay=0,length=fibreLen, models={"myCDelayModel": FibreDelayModel(c=cSpeed)})
MyCChannel2= ClassicalChannel("CChannel_A->B",delay=0,length=fibreLen, models={"myCDelayModel": FibreDelayModel(c=cSpeed)})

nodeB.connect_to(nodeA, MyCChannel, local_port_name="portCB_1", remote_port_name="portCA_2")
nodeA.connect_to(nodeB, MyCChannel2, local_port_name="portCA_1", remote_port_name="portCB_2")

nodeA.connect_to(nodeB, MyCChannel2, local_port_name="portCA_1", remote_port_name="portCB_2")