import numpy as np
import networkx as nx

gene_length=7
def make_gene(length):
    alphabet="0123456789abcdef"
    gene=""
    for i in range(length):
        rand=np.random.randint(len(alphabet))
        gene+=alphabet[rand]
    return gene

class individual:
    
    def __init__(self, gene_number):
        self.genome=""
        for i in range(gene_number):
            self.genome+=make_gene(gene_length)
        genome_length=len(self.genome)
        self.binary=""
        for i in range(genome_length):
            self.binary+=format(int(self.genome[i], 16), '04b')
        
    
    def binary(self, genome):
        genome_length=len(self.genome)
        self.binary=""
        for i in range(genome_length):
            self.binary+=format(int(self.genome[i], 16), '04b')
        return self.binary
    
class input_node:
    def __init__(self, ID):
        self.ID=ID
        self.initial=0
        self.updated=0
    

class internal_node:
    def __init__(self, ID):
        self.ID=ID
        self.initial=0
        self.updated=0
        
    def sum_inputs(self, graph):
        #Function that reads connections from genome
        #Then sums over connections to this node, from values of connected nodes times edge weights
        
        neighborlist=list(nx.neighbors(graph, self))
        inputsum=0
        
        for neighbor in neighborlist:
            path=(self, neighbor)
            edge_dict=graph.get_edge_data(*path)
            edgeweight=edge_dict.get('weight')
            inputsum=inputsum+edgeweight*neighbor.initial
        
        return inputsum
        
    def sig(self, inputsum):
        return 2/(1+np.e**(-inputsum))-1
    
    def update(self):
        self.initial=self.updated
    
class output_node:
    def __init__(self, ID):
        self.ID=ID
        self.initial=0
        self.updated=0
    
    def sum_inputs(self, graph):
        #Function that reads connections from genome
        neighborlist=list(nx.neighbors(graph, self))
        inputsum=0
        
        for neighbor in neighborlist:
            path=(self, neighbor)
            edge_dict=graph.get_edge_data(*path)
            edgeweight=edge_dict.get('weight')
            inputsum=inputsum+edgeweight*neighbor.initial
        
        return inputsum
        
    def prob(self, inputsum):
        return 1/(1+np.e**(-inputsum))
    
    def update(self):
        self.initial=self.updated
