from netsquid.components.switch import Switch, SimpleSwitch
from netsquid.components.component import Component, Message

# Switch implemented with netsquid design for star topology network

class ClassicSwitch(Switch):
    def __init__(self, name, topology: {str: str}): #node as input_port : output_port
        ports = list(topology.keys()) + list(topology.values())
        super(ClassicSwitch, self).__init__(name, port_names=ports)
        self._topology = topology

    @property
    def topology(self):
        """dict: The mapping from node to his input port."""
        return self._topology

    @topology.setter
    def topology(self, value):
        self._topology = value

    def routing_table(self, input_port, message) -> [(Message, str)]:
        dest = message.meta["destination"]
        return [(message, self.topology[dest])]