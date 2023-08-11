#Utils funcions for Measurement Device Independent QKD protocol. Based on NetSquid library
# Utils functions used by client nodes that want negotiate a key with MDI-QKD protocol

def measurement_result_eval(init, chosen_basis, chosen_bit, mdi_result):
    # It takes in input a init flag (true if the client node is the initializer, false if not),
    # which basis and bit the client had chosen to prepare the qubit sent to the mdi node
    # and last the results of the measurements published by the mdi node.
    # After the evaluation of the results based on the interference of the two qubits in the mdi node,
    # the function return the negotiated bit shared by the two clients
    # If the results are not usable then the function will return None
    # The evaluation follows the scheme explained in doi:10.1103/PhysRevLett.108.130503
    # and in doi:10.3390/electronics7040049

        # Evaluation if client have choose the rectilinear base
    if chosen_basis == rectilinear:
        if result == "cvch" or result == "dvdh" or result == "cvdh" or result == "chdv":
            if init: 
                return int(chosen_bit)
            else:
                # bit flip necessary in order to get the same bit as the init client
                return int(not chosen_bit)
        else:
            return None
            
        # Evaluation if client have choose the digonal base
    if chosen_basis == diagonal:
        if result == "cvch" or result == "dvdh":
            return int(chosen_bit)
        else if result == "chdv" or result == "cvdh":
            if init: 
                return int(chosen_bit)
            else:
                # bit flip necessary in order to get the same bit as the init client
                return int(not chosen_bit) 
        else:
            return None

    return None