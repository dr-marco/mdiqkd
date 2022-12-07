import netsquid as ns
from netsquid.protocols import NodeProtocol

class clientProtocol(NodeProtocol):
    def __init__(self, node, status=0):
        super().__init__()
        self.num_bits=num_bits
        self.node = node
        self.status = status
        self.portNameQ1=port_names[0] #left arm
        self.portNameQ2=port_names[1] #right arm
        self.portNameC1=port_names[2] #from
        self.portNameC2=port_names[3] #to
        self.HbasisList=Random_basis_gen(self.num_bits)
        self.XbasisList=Random_basis_gen(self.num_bits)
        self.loc_measRes=[]
        self.key=[]
        self.sourceQList=[]

    def start_protocol():
        #do stuff for initialize protocol
        return null


    def run():
        #wait for init 
        #set if flip bit is required
        #random bit and basis
        #send quit and wait result
        #publish basis chosen and wait other part's basis
        #generate the correct key
        return null