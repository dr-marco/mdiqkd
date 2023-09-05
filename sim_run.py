import netsquid as ns
from netsquid.nodes.node import Node
from netsquid.components.cchannel import ClassicalChannel
from netsquid.components.models import  FibreDelayModel
from netsquid.components.cqchannel import CombinedChannel
#from netsquid.components.qchannel import QuantumChannel
from netsquid.components.models.qerrormodels import FibreLossModel
import mdi_node as mdi
import client_node as client
from switch import ClassicSwitch

# Config flag
fibreLen = 20 # length of the fiber channel
quantumLen = 20 # length of the quantum channel. This is used for both Alice and Bob
cSpeed=2*10**5 # speed of light of fiber channel
error_models = {"delay_model": FibreDelayModel(c=cSpeed), 'quantum_loss_model':FibreLossModel(p_loss_init=0, p_loss_length=0.2)}
num_bits_sim = 1000
# Reset of the simulation
ns.sim_reset()
ns.set_random_state(seed=56)

# Declaration of the nodes
nodeA = Node("Alice",   port_names=["portCQ","portC_mdi","portC_out","portC_in"])
nodeB = Node("Bob"  ,   port_names=["portCQ","portC_mdi","portC_out","portC_in"])
nodeC = Node("Charlie", port_names=["portCQ","portC_mdi","portC_out","portC_in"])
nodeD = Node("Dave",    port_names=["portCQ","portC_mdi","portC_out","portC_in"])

mdi_node = Node("mdi", port_names=["portQ_1", "portC_1","portQ_2","portC_2", "portQ_3","portC_3", "portQ_3","portC_3"])

# ------------------------------ NEW IMPLEMENTATION: switch ------------------------------
switch_node = ClassicSwitch("switch_node", topology={"Alice":"Alice_route", "Bob":"Bob_route", "Charlie": "Charlie_route", "Dave": "Dave_route"})

#Classical connection between switch node and client nodes
CChannel_B_switch = ClassicalChannel("CChannel_B->switch",
                                length=fibreLen,
                                models={"CDelayModel": FibreDelayModel(c=cSpeed)})
CChannel_switch_B = ClassicalChannel("CChannel_switch->B",
                                length=fibreLen,
                                models={"CDelayModel": FibreDelayModel(c=cSpeed)})
CChannel_A_switch = ClassicalChannel("CChannel_A->switch",
                                length=fibreLen,
                                models={"CDelayModel": FibreDelayModel(c=cSpeed)})
CChannel_switch_A = ClassicalChannel("CChannel_switch->A",
                                length=fibreLen,
                                models={"CDelayModel": FibreDelayModel(c=cSpeed)})
CChannel_C_switch = ClassicalChannel("CChannel_C->switch",
                                length=fibreLen,
                                models={"CDelayModel": FibreDelayModel(c=cSpeed)})
CChannel_switch_C = ClassicalChannel("CChannel_switch->C",
                                length=fibreLen,
                                models={"CDelayModel": FibreDelayModel(c=cSpeed)})
CChannel_D_switch = ClassicalChannel("CChannel_D->switch",
                                length=fibreLen,
                                models={"CDelayModel": FibreDelayModel(c=cSpeed)})
CChannel_switch_D = ClassicalChannel("CChannel_switch->D",
                                length=fibreLen,
                                models={"CDelayModel": FibreDelayModel(c=cSpeed)})

nodeB.ports["portC_out"].connect(CChannel_B_switch.ports["send"])
nodeB.ports["portC_in"].connect(CChannel_switch_B.ports["recv"])
nodeA.ports["portC_out"].connect(CChannel_A_switch.ports["send"])
nodeA.ports["portC_in"].connect(CChannel_switch_A.ports["recv"])
nodeC.ports["portC_out"].connect(CChannel_C_switch.ports["send"])
nodeC.ports["portC_in"].connect(CChannel_switch_C.ports["recv"])
nodeD.ports["portC_out"].connect(CChannel_D_switch.ports["send"])
nodeD.ports["portC_in"].connect(CChannel_switch_D.ports["recv"])

switch_node.ports["Bob"].connect(CChannel_B_switch.ports["recv"])
switch_node.ports["Bob_route"].connect(CChannel_switch_B.ports["send"])
switch_node.ports["Alice"].connect(CChannel_A_switch.ports["recv"])
switch_node.ports["Alice_route"].connect(CChannel_switch_A.ports["send"])
switch_node.ports["Charlie"].connect(CChannel_C_switch.ports["recv"])
switch_node.ports["Charlie_route"].connect(CChannel_switch_C.ports["send"])
switch_node.ports["Dave"].connect(CChannel_D_switch.ports["recv"])
switch_node.ports["Dave_route"].connect(CChannel_switch_D.ports["send"])

#Classical connection between mdi node and client nodes
CChannel_mdi_A = ClassicalChannel("CChannel_mdi->A",
                                length=fibreLen,
                                models={"CDelayModel": FibreDelayModel(c=cSpeed)}) 
CChannel_mdi_B = ClassicalChannel("CChannel_mdi->B",
                                length=fibreLen,
                                models={"CDelayModel": FibreDelayModel(c=cSpeed)})
CChannel_mdi_C = ClassicalChannel("CChannel_mdi->C",
                                length=fibreLen,
                                models={"CDelayModel": FibreDelayModel(c=cSpeed)})
CChannel_mdi_D = ClassicalChannel("CChannel_mdi->D",
                                length=fibreLen,
                                models={"CDelayModel": FibreDelayModel(c=cSpeed)})

mdi_node.connect_to(nodeA, CChannel_mdi_A, local_port_name="portC_1", remote_port_name="portC_mdi")
mdi_node.connect_to(nodeB, CChannel_mdi_B, local_port_name="portC_2", remote_port_name="portC_mdi")
mdi_node.connect_to(nodeC, CChannel_mdi_C, local_port_name="portC_3", remote_port_name="portC_mdi")
mdi_node.connect_to(nodeD, CChannel_mdi_D, local_port_name="portC_4", remote_port_name="portC_mdi")

#Classical-Quantum connection from Alice and Bob to MDI node
CQChannel_A = CombinedChannel(name='QChannel_A',
                                length=quantumLen,
                                models=error_models
                            )

CQChannel_B = CombinedChannel(name='QChannel_B',
                                length=quantumLen,
                                models=error_models
                            )

CQChannel_C = CombinedChannel(name='QChannel_C',
                                length=quantumLen,
                                models=error_models
                            )

CQChannel_D = CombinedChannel(name='QChannel_D',
                                length=quantumLen,
                                models=error_models
                            )

nodeA.connect_to(mdi_node, CQChannel_A, local_port_name="portCQ", remote_port_name="portQ_1")
nodeB.connect_to(mdi_node, CQChannel_B, local_port_name="portCQ", remote_port_name="portQ_2")
nodeC.connect_to(mdi_node, CQChannel_C, local_port_name="portCQ", remote_port_name="portQ_3")
nodeD.connect_to(mdi_node, CQChannel_D, local_port_name="portCQ", remote_port_name="portQ_4")

# Measurement device independent protocol
mdi_protocol = mdi.mdiProtocol(mdi_node, client_nodes=["Alice", "Bob", "Charlie", "Dave"],
                                quantum_port_names=["portQ_1", "portQ_2","portQ_3","portQ_4"], classic_port_names=["portC_1", "portC_2","portC_3","portC_4"])

# Client nodes protocols
alice_protocol = client.clientProtocol(nodeA, num_bits=num_bits_sim, init=True, other_nodes=["Bob", "Dave"])
bob_protocol = client.clientProtocol(nodeB, num_bits=num_bits_sim, init=False, other_nodes=[])
charlie_protocol = client.clientProtocol(nodeC, num_bits=num_bits_sim, init=True, other_nodes=["Alice"])
dave_protocol = client.clientProtocol(nodeD, num_bits=num_bits_sim, init=True, other_nodes=["Bob"])
# start the mdi protocol
mdi_protocol.start()
# start the client protocols
alice_protocol.start()
bob_protocol.start()
charlie_protocol.start()
dave_protocol.start()


# execute the protocol 
stats = ns.sim_run()

print("End of simulation")
print("Nodes generated keys")
print(nodeA.name + "'s keys:\t" + str(alice_protocol.keys))
print(nodeB.name + "'s keys:\t" + str(bob_protocol.keys))
print(nodeC.name + "'s keys:\t" + str(charlie_protocol.keys))
print(nodeD.name + "'s keys:\t" + str(dave_protocol.keys))
print("EOF")