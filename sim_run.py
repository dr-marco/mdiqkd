import netsquid as ns
from netsquid.nodes.node import Node
from netsquid.components.cchannel import ClassicalChannel
from netsquid.components.models import  FibreDelayModel
from netsquid.components.cqchannel import CombinedChannel
from netsquid.components.models.qerrormodels import FibreLossModel
import mdi_node as mdi
import client_node
from switch import ClassicSwitch
import net_utils as nu
import json
from exgaussian_fiber_delay_model import ExGaussianFibreDelayModel

# Config flag for reaction delay model
mu = 5             # Media per la parte gaussiana
sigma = 0.05         # Deviazione standard per la parte gaussiana
lambd = 1.5          # Parametro lambda per la parte esponenziale

# Config flag
fibreLen = 40 # length of the fiber channel
quantumLen = 40 # length of the quantum channel. This is used for both Alice and Bob
num_bits_sim = 10000 # number of qubits prepared during a qkd protocol execution
delay_wait = 800000
cSpeed=2*10**5 # speed of light of fiber channel
#error_models = {"delay_model": ExGaussianFibreDelayModel(c=cSpeed, mu=mu, sigma=sigma, lambd=lambd), 'quantum_loss_model':FibreLossModel(p_loss_init=0, p_loss_length=0.2)}
error_models = {"delay_model": FibreDelayModel(c=cSpeed), 'quantum_loss_model':FibreLossModel(p_loss_init=0, p_loss_length=0.2)}


# Load nodes from json file
with open("client_nodes_db.json", "r") as f:
    data = json.load(f)

client_nodes=[]
init={}
other_nodes={}
for client in data["client_nodes"]:
    for key in client.keys():
        client_nodes.append(key)
        client_dict = client[key]
        init[key] = client_dict["init"]
        other_nodes[key] = client_dict["other_nodes"]

node_objects = []
node_protocol_objects = []
# Reset of the simulation
ns.sim_reset()
ns.set_random_state(seed=56)

# Declaration of the nodes
topology = nu.gen_topology(client_nodes)
mdi_ports = nu.gen_mdi_ports(client_nodes)

mdi_node = Node("mdi", port_names=nu.get_classic_ports(mdi_ports) + nu.get_quantum_ports(mdi_ports))
switch_node = ClassicSwitch("switch_node", topology=topology)

for client in client_nodes:
    node_ = Node(client, port_names=["portCQ","portC_mdi","portC_out","portC_in"])

    #Classical connection between switch node and client nodes
    switch_channel_names = nu.gen_switch_channel_names(client)
    CChannel_switch_node = ClassicalChannel(switch_channel_names[0],
                                    length=fibreLen,
                                    models={"delay_model": FibreDelayModel(c=cSpeed)})
    CChannel_node_switch = ClassicalChannel(switch_channel_names[1],
                                    length=fibreLen,
                                    models={"delay_model": FibreDelayModel(c=cSpeed)})

    node_.ports["portC_out"].connect(CChannel_node_switch.ports["send"])
    node_.ports["portC_in"].connect(CChannel_switch_node.ports["recv"])

    switch_node.ports[client].connect(CChannel_node_switch.ports["recv"])
    switch_node.ports[topology[client]].connect(CChannel_switch_node.ports["send"])

    #Classical connection between mdi node and client nodes
    mdi_channel_names = nu.gen_mdi_channel_names(client)
    CChannel_mdi_node = ClassicalChannel(mdi_channel_names[0],
                                    length=fibreLen,
                                    models={"delay_model": FibreDelayModel(c=cSpeed)}) 

    mdi_node.connect_to(node_, CChannel_mdi_node, local_port_name=mdi_ports[client][0], remote_port_name="portC_mdi")

    #Classical-Quantum connection from clients to MDI node
    CQChannel_node = CombinedChannel(name=mdi_channel_names[1],
                                    length=quantumLen,
                                    models=error_models
                                )

    node_.connect_to(mdi_node, CQChannel_node, local_port_name="portCQ", remote_port_name=mdi_ports[client][1])
    node_objects.append(node_)
    node_protocol = client_node.clientProtocol(node_, num_bits=num_bits_sim, delay_for_wait = delay_wait, init=init[client], other_nodes=other_nodes[client])
    node_protocol.start()
    node_protocol_objects.append(node_protocol)

# Measurement device independent protocol
mdi_protocol = mdi.mdiProtocol(mdi_node, client_nodes=client_nodes,
                                quantum_port_names=nu.get_quantum_ports(mdi_ports), classic_port_names=nu.get_classic_ports(mdi_ports))

mdi_protocol.start()
cumulative_stat = {}
# execute the simulation 
stats = ns.sim_run()
print("End of simulation")
print("Nodes generated keys")
sim_stat = {}
for node_prot in node_protocol_objects:
    print(str(node_prot.node.name) + "'s keys:\t" + str(node_prot.keys))
    #print(str(node_prot.node.name) + "'s time stats:\t" + str(node_prot.time_stats))
    sim_stat[str(node_prot.node.name)+ "'s keys"] = node_prot.time_stats
cumulative_stat[0] = sim_stat
ns.sim_reset()

with open("simulation_results_db.json", "w") as r:
    json.dump(cumulative_stat, r, indent = 4)
    
print("EOF")