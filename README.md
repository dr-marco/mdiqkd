# mdiqkd 

Simulation of the protocol Measurement-Device-Independent Quantum Key Distribution using NetSquid

__Alert__:ATM the updates are not finished and results could be wrong 

### Update 2023-08-27 

Completed the first working simulation network, two nodes (alice and bob) and a central mdi node. It could be better but it is kinda usable

Next steps: 
- ~~Change the Client-Mdi connection from Quantum to Combined channel~~
- Improve and tune delay and loss models
- Modify the protocols in order to be more flexible and more _general purpouse_ :arrow_right: in progress
- Simulation network with more than two client :arrow_right: in progress

#### Mid-Update 2023-08-31

Snapshot of the first working simulation network as pre-release v0.0.1 to save it for the future 

Added __switch__ component to change the network topology among all clients nodes from fully connected network to a star topology with the switch as a center node. The network is yet work in progress and many fix are needed

### Usage

You can work with the sim_run.py file where you can modify some parameter if desired. You can run it simply with

```python sim_run.py```

[!] __Attention__: Netsquid library required and tested only with Python 3.9