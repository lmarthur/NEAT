import networkx as nx

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
    nx.draw(G, with_labels=False)
    return G