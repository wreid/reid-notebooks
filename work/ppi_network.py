#!/usr/bin/env

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sys import argv
from sys import exit

def main(args):
    input_file1 = args[1]
    input_file2 = args[2]

    inp1 = sanitize_name(input_file1)
    inp2 = sanitize_name(input_file2)

    Y = nx.Graph()
    H = nx.Graph()

    load_txt(inp2, Y)
    del_dupl(Y)

    load_txt(inp1, H)
    del_dupl(H)

    print '\nYEAST'
    MY = largest_component(Y)

    print 'HUMAN'
    MH = largest_component(H)

    plt.xlabel('Degree', fontsize=14, color='black')
    plt.ylabel('Frequency', fontsize=14, color='black')
    plt.title('PPI of Human and Yeast genomes (BioGrid)', fontsize=16, color='black')
    plt.autoscale(enable=True)
    n1, bins1, patches1 = plt.hist(nx.degree(MY).values(), \
        bins=np.max(nx.degree(MY).values())/25, log=True, histtype='bar', \
        color='red', alpha=.8)
    n2, bins2, patches2 = plt.hist(nx.degree(MH).values(), \
        bins=np.max(nx.degree(MH).values())/25, log=True, histtype='bar', \
        color='black', alpha=.3)
    d, p = stats.ks_2samp(n1, n2)
    print 'D value of %f' % d
    print 'P value of %f' % p
    plt.show()
    plt.close()


def sanitize_name(filen):
    try:
        inp = str(filen)
    except TypeError:
        print 'Input file name must be a string.'
        exit()
    return inp

def load_txt(fname, graph):
    """
    loads text from a file, removes whitespace and loads
    each line as two nodes connected by an edge
    """
    f = open(fname, 'rb')
    txt = f.readlines()

    for line in txt:
        line.strip()
        l = tuple(line.split())
        if l[0] != l[1]:
            graph.add_edge(*l)


def del_dupl(graph):
    """
    iterates through graph, deleting duplicate edges
    """
    for edge in graph.edges():
        if edge[0] == edge[1]:
            graph.remove_edge(edge[0], edge[1])


def largest_component(graph):
    """
    makes a new graph of the largest component in the input graph
    """
    # find and output graph
    graphs = sorted(list(nx.connected_component_subgraphs(graph, copy=True)), key=len, reverse=True)
    out_graph = graphs[0]

    # print info about removed
    removed = 0
    for subgraph in graphs[1:]:
        removed = removed + len(subgraph.nodes())
    print '%d nodes removed' % removed
    print '%d components removed' % len(graphs[1:])
    print '%d nodes and %d edges in main component\n' % (len(out_graph.nodes()), \
        len(out_graph.edges()))

    return out_graph
    
    


if __name__ == '__main__':
    main(argv)