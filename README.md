# mdiqkd 

Simulation of the protocol Measurement-Device-Independent Quantum Key Distribution using NetSquid

~~ATM the system is not finished and results will be wrong. Don't use it~~ 

### Update 2023-08-27 

Completed the first working simulation network, two nodes (alice and bob) and a central mdi node. It could be better but it is kinda usable

Next steps: 
- Change the Client-Mdi connection from Quantum to Combined channel
- Improve and tune delay and loss models
- Modify the protocols in order to be more flexible and more _general purpouse_
- Simulation network with more than two client

### Usage

You can work with the sim_run.py file where you can modify some parameter if desired. You can run it simply with

```python sim_run.py```

[!] __Attention__: Netsquid library required and tested with Python 3.9