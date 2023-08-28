import random
import netsquid as ns

#Utils funcions for Measurement Device Independent QKD protocol. Based on NetSquid library
# Utils functions used by client nodes that want negotiate a key with MDI-QKD protocol

def measurement_result_eval(init, chosen_basis, chosen_bit, result):
    # It takes in input a init flag (true if the client node is the initializer, false if not),
    # which basis and bit the client had chosen to prepare the qubit sent to the mdi node
    # and last the results of the measurements published by the mdi node.
    # After the evaluation of the results based on the interference of the two qubits in the mdi node,
    # the function return the negotiated bit shared by the two clients
    # If the results are not usable then the function will return None
    # The evaluation follows the scheme explained in doi:10.1103/PhysRevLett.108.130503
    # and in doi:10.3390/electronics7040049

        # Evaluation if client have choose the rectilinear base
    if chosen_basis == 0:
        if result == "cvch" or result == "dvdh" or result == "cvdh" or result == "chdv":
            if init: 
                return int(chosen_bit)
            else:
                # bit flip necessary in order to get the same bit as the init client
                return int(not chosen_bit)
        else:
            return None
            
        # Evaluation if client have choose the digonal base
    if chosen_basis == 1:
        if result == "cvch" or result == "dvdh":
            return int(chosen_bit)
        elif result == "chdv" or result == "cvdh":
            if init: 
                return int(chosen_bit)
            else:
                # bit flip necessary in order to get the same bit as the init client
                return int(not chosen_bit) 
        else:
            return None

    return None


def random_basis_gen(length):
    # Return a list of ones and zeros randomly chosen. Method used for qubit preparation
    return [random.randint(0,1) for i in range(length)]

def random_start_time(end=10000000):
    # Return a random time instant from 0 to end time. Method used for the start of the protocol
    return random.randint(0,end)

def generate_quantum_photon(chosen_bit, chosen_basis):
    # Return a photon with polarization of 0, 45, 90 or 135 degree based on bit and basis chosen
    qubits = ns.qubits.create_qubits(1) #generate a qubit in state |0>
    qubit = qubits[0]
    if chosen_bit%2==1:
        ns.qubits.operate(qubit, ns.X) #apply negation i.e. from 0 to 1 if applied
    if chosen_basis%2==1:
        ns.qubits.operate(qubit, ns.H) #apply Hadamard gate to switch basis
    return qubit