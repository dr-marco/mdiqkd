def gen_topology(clients):
    topology = {}
    for client in clients:
        topology[client] = "".join(client + "_route")
    return topology

def gen_mdi_ports(clients):
    ports = {}
    for client in clients:
        ports[client] = ("".join("portC_" + client),"".join("portQ_" + client))
    return ports

def get_quantum_ports(mdi_ports):
    quantum_ports = []
    for client in mdi_ports.values():
        quantum_ports.append(client[1])
    return quantum_ports

def get_classic_ports(mdi_ports):
    classic_ports = []
    for client in mdi_ports.values():
        classic_ports.append(client[0])
    return classic_ports

def gen_switch_channel_names(client):
    to_switch = "".join(client + "->switch")
    from_switch = "".join("switch->" + client)
    return (from_switch, to_switch)

def gen_mdi_channel_names(client):
    to_mdi = "".join(client + "->mdi")
    from_mdi = "".join("mdi->" + client)
    return (from_mdi, to_mdi)

