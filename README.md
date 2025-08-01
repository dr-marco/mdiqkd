# mdiqkd 

Simulation of the protocol Measurement-Device-Independent Quantum Key Distribution using NetSquid

> [!WARNING] 
> ATM the updates are not finished and results could be wrong

### Usage

You can work with the __json__ file, where you can modify the network, and the ``sim_run.py`` file, where you can modify some default parameter if desired. You can run it simply with

```python sim_run.py```

You can set some parameters into the python command. For more information about this you can run the help command:

```python sim_run.py -h```

The network description is described into the json file ```client_nodes_db.json```. Each element is a node and contains a ```init``` flag and a list of ```other_nodes``` to run the protocol against. The current json file can be used as example of a valid network.

> [!NOTE] 
> Netsquid library required and tested only with Python 3.9

## Updates

### Update 2024-11-18

Solved some tricky bugs that raise some errors in the simulations. Added some try-catch in the code to manage possible errors during execution. 

Added functionality to select the current execution run number. This allows you to save multiple simulation runs in the same JSON output file by assigning a unique key for each run. This is especially useful when using a wrapper or running the simulator multiple times.

Next steps:

- Optional refactor (may not happen but never say never)
- ~~Add wrapper for multiple simulations~~ edit: wrote a bash script as wrapper for my personal scope. Anyway CLI parameters implemented
- ~~Solve bug with some possible race conditions during runs~~ edit: bug solved by abort system implementation 

### Update 2024-10-10 (edit 2024-11-07)

Still alive. Added the new model that create the delay considering the length of the fiber cable and the reaction time of the photon source. The reaction time model
follows an [ex-gaussian distribution](https://en.wikipedia.org/wiki/Exponentially_modified_Gaussian_distribution). 
Used ```argparse``` library to tune config parameter in the command line. Useful for scripting the program with a wrapper.

### Update 2023-09-04

Quite big update. Modified the mdi and clients protocols in order to be able to perform the simulation

- with more than two nodes i.e. simulation network can be built with any number of nodes
- with more than one qkd run for node i.e. each node can perform an arbitrary number of run with other nodes, simply putting the queue in the ```other_nodes``` list
- with more than one initializer i.e. multiple nodes can start the mdiqkd protocol if ```init``` is set ```True``` (This could be done also before but only twice between Alice and Bob)

The simulation should work quite fine but it is not obvious that everything works perfectly. There may be some ~~bullshits~~ emm, flaws and bugs in the design. Hope to fix them soon. So, once again, be careful with this code

The current network consists of four client nodes: Alice, Bob, Charlie and Dave. It is described in the json file ```client_nodes_db.json```

#### Mid-Update 2023-08-31

Snapshot of the first working simulation network as pre-release v0.0.1 to save it for the future 

Added __switch__ component to change the network topology among all clients nodes from fully connected network to a star topology with the switch as a center node. The network is yet work in progress and many fixes are needed

### Update 2023-08-27 

Completed the first working simulation network, two nodes (alice and bob) and a central mdi node. It could be better but it is kinda usable