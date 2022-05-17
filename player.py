import networkx as nx
import random

from individual import individual, input_node, internal_node, output_node

depth=10

input_number=3
internal_number=3
output_number=3
genome_length=input_number+internal_number+output_number

#create test individual
test=individual(genome_length)

#Create input, internal, andn output node lists
def get_nodes(individual):
    input_nodes=[]
    for i in range(input_number):
        input_nodes.append(input_node(i))

    internal_nodes=[]
    for i in range(internal_number):
        internal_nodes.append(internal_node(i))

    output_nodes=[]
    for i in range(output_number):
        output_nodes.append(output_node(i))

    return input_nodes, internal_nodes, output_nodes


def get_action(individual):

    nodes=get_nodes(individual)
    input_nodes=nodes[0]
    internal_nodes=nodes[1]
    output_nodes=nodes[2]



    def elist_construct(individual):

        elist=[]

        for i in range(genome_length):
            binarygene=test.binary[(i)*28:(i+1)*28]
            origin_class=int(binarygene[0])
            origin_node_num=int(binarygene[1:8], 2)
            arrival_class=int(binarygene[8])
            arrival_node_num=int(binarygene[9:16], 2)
            weight_sign=int(binarygene[16])
            weight=int(binarygene[16:], 2)/1024
            if weight_sign==0:
                weight=-int(binarygene[16:], 2)/1024
            if origin_class==0:
                origin_node=input_nodes[origin_node_num % len(input_nodes)]
            if origin_class==1:
                origin_node=internal_nodes[origin_node_num % len(internal_nodes)]
            if arrival_class==0:
                arrival_node=internal_nodes[arrival_node_num % len(internal_nodes)]
            if arrival_class==1:
                arrival_node=output_nodes[arrival_node_num % len(output_nodes)]
            edge=(origin_node, arrival_node, weight)
            elist.append(edge)

        return elist


    def network_construct(individual):
        G=nx.Graph()
        elist=[]

        for i in range(genome_length):
            binarygene=test.binary[(i)*28:(i+1)*28]
            origin_class=int(binarygene[0])
            origin_node_num=int(binarygene[1:8], 2)
            arrival_class=int(binarygene[8])
            arrival_node_num=int(binarygene[9:16], 2)
            weight_sign=int(binarygene[16])
            weight=int(binarygene[16:], 2)/1024
            if weight_sign==0:
                weight=-int(binarygene[16:], 2)/1024
            if origin_class==0:
                origin_node=input_nodes[origin_node_num % len(input_nodes)]
            if origin_class==1:
                origin_node=internal_nodes[origin_node_num % len(internal_nodes)]
            if arrival_class==0:
                arrival_node=internal_nodes[arrival_node_num % len(internal_nodes)]
            if arrival_class==1:
                arrival_node=output_nodes[arrival_node_num % len(output_nodes)]
            edge=(origin_node, arrival_node, weight)
            elist.append(edge)
        G.add_weighted_edges_from(elist)
        #nx.draw(G, with_labels=False)
        return G


    #construct network representation
    elist=elist_construct(test)
    G=network_construct(test)
    nodelist=list(nx.nodes(G))
    #print(nodelist)

    #Iterate over depth, repeat update process for #depth times
    for i in range(depth):
    #Iterate over nodes to calculate inputs for update
        for node in internal_nodes:
            if node in nodelist:
                inputsum=node.sum_inputs(G)
                node.updated=node.sig(inputsum)

        for node in output_nodes:
            if node in nodelist:
                inputsum=node.sum_inputs(G)
                node.updated=node.prob(inputsum)

        #Update stored values
        for node in internal_nodes:
            if node in nodelist:
                node.initial=node.updated

        for node in output_nodes:
            if  node in nodelist:
                node.initial=node.updated

    actionlist=list()
    weightlist=list()
    for node in output_nodes:
        if node in nodelist:
            actionlist.append(node.ID)
            weightlist.append(node.updated)
            #print("ID =", node.ID, ", Node Value =",  node.updated)

    #print(actionlist)
    #print(weightlist)
    action=random.choices(actionlist, weightlist)
#    print("Action:", * action)
    return action[0]

action=get_action(test)
