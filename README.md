# mdiqkd 

Simulation of the protocol Measurement-Device-Independent Quantum Key Distribution using NetSquid

### Usage

You can work with the __json__ file, where you can modify the network, and the ``sim_run.py`` file, where you can modify some default parameter if desired. You can run it simply with

```python sim_run.py```

You can set some parameters into the python command. For more information about this you can run the help command:

```python sim_run.py -h```

The network description is described into the json file ```client_nodes_db.json```. Each element is a node and contains a ```init``` flag and a list of ```other_nodes``` to run the protocol against. The current json file can be used as example of a valid network.

> [!NOTE] 
> Netsquid library required and tested only with Python 3.9