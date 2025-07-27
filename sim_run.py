import netsquid as ns
from netsquid.nodes.node import Node
from netsquid.components.cchannel import ClassicalChannel
from netsquid.components.models import  FibreDelayModel
from netsquid.components.cqchannel import CombinedChannel
from netsquid.components.models.qerrormodels import FibreLossModel, DephaseNoiseModel #TODO add dephase error in simulations
import mdi.mdi_node as mdi
import client.client_node as client_node
from network.switch import ClassicSwitch
import network.net_utils as nu
import json
import argparse
import pathlib
import os
from models.exgaussian_fiber_delay_model import ExGaussianFibreDelayModel as ExGaussianFibreDelayModel

# Argparse lib functionality
parser = argparse.ArgumentParser(prog='sim_run.py',
                                description=
                                'A quantum network simulation processing the measurement device independent quantum key distribution.')
parser.add_argument('-i', '--inputdb', type=pathlib.Path,
                    help='input database with the network configuration')

parser.add_argument('-o', '--outputdb', type=pathlib.Path,
                    help='output database with results of the simulation')

parser.add_argument('-dm', '--delaymodel', choices=['fiber', 'exgaussian'], default='fiber',
                    help='delay model for trasmission through fiber channel')

parser.add_argument('-fl', '--fiberlen', type=float, default=40,
                    help='length in kilometers of the fiber cables for classical communications')

parser.add_argument('-ql', '--quantumlen', type=float, default=40,
                    help='length in kilometers of the fiber cables for quantum communications')

parser.add_argument('-nb', '--nbits', type=int, default=1000,
                    help='number of qubits prepared during a qkd protocol execution')

parser.add_argument('-nr', '--nrun', type=int, default=0,
                    help='number of current simulation iteration. Useful to save correctly in one json output file')

parser.add_argument('-mu', '--mu', type=float, default=10,
                    help='mean of gaussian part for reaction delay model')

parser.add_argument('-sg', '--sigma', type=float, default=0.1,
                    help='standard deviation of gaussian part for reaction delay model')

parser.add_argument('-lb', '--lambd', type=float, default=1.5,
                    help='lambda decay of exponential part for reaction delay model')
args = parser.parse_args()

# Input-Output-Config files names
if args.inputdb != None:
    client_nodes_db = args.inputdb
else:
    client_nodes_db = "client_nodes_db.json" # default value
if args.outputdb != None:
    simulation_results_db = args.outputdb
else:
    simulation_results_db = "simulation_results_db.json" # default value

# Config flag for reaction delay model
mu = args.mu                # (default 10) Mean of gaussian part
sigma = args.sigma          # (defualut 0.1) Standard deviation of gaussian part
lambd = args.lambd          # (default 1.5) lambda decay of exponential part

# Config flag
fibreLen = args.fiberlen            # (default 40) length of the fiber channel
quantumLen = args.quantumlen        # (default 40) length of the quantum channel. This is used for both Alice and Bob
num_bits_sim = args.nbits           # (default 1000) number of qubits prepared during a qkd protocol execution
delay_wait = 1e4 * fibreLen
cSpeed=2*10**5                      # speed of light of fiber channel
if args.delaymodel == 'fiber':
    error_models = {"delay_model": FibreDelayModel(c=cSpeed), 'quantum_loss_model':FibreLossModel(p_loss_init=0, p_loss_length=0.2)}
elif args.delaymodel == 'exgaussian':
    error_models = {"delay_model": ExGaussianFibreDelayModel(c=cSpeed, mu=mu, sigma=sigma, lambd=lambd), 'quantum_loss_model':FibreLossModel(p_loss_init=0, p_loss_length=0.2)}


# Load nodes from json file
with open(client_nodes_db, "r") as f:
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
    node_protocol = client_node.clientProtocol(node_, num_bits=num_bits_sim, delay_for_wait = delay_wait, delay_for_first=2e4 * fibreLen, init=init[client], other_nodes=other_nodes[client])
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

if os.path.isfile(simulation_results_db):
    with open(simulation_results_db, "r") as f:
        cumulative_stat = json.load(f)
nrun = args.nrun
cumulative_stat[nrun] = sim_stat
ns.sim_reset()

with open(simulation_results_db, "w") as r:
    json.dump(cumulative_stat, r, indent = 4)
    
print("EOF")