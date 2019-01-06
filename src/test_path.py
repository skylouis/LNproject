import numpy as np
import networkx as nx
import random
import json
from LN_graph import LN_graph

#%%
graph = json.load(file('../LN_snapshot/graph.json','rw'))

LN_nodes = graph['nodes']
LN_edges = graph['edges']

graph = LN_graph()

graph.add_nodes(LN_nodes)
graph.add_edges(LN_edges)

#%%
def get_route_fees(path, amount):
    total_fees = 0
    new_amount = amount
    for i in reversed(range(1,len(path))):
        fees = graph.fee_tranfert(path[i-1],path[i],new_amount)
        total_fees += fees
        new_amount += fees
    
    return total_fees


def get_all_paths(node1_pub, node2_pub, route_length):
    paths = list(nx.all_simple_paths(graph.nx_graph, node1_pub, node2_pub, cutoff=route_length))
    return paths


def test_random(amount):
    print ">>> [1/4] Node generation..."
    node1_pub = random.choice(LN_nodes)['pub_key']
    node2_pub = node1_pub
    while (node2_pub == node1_pub):
        node2_pub = random.choice(LN_nodes)['pub_key']
        
    print ">>> [2/4] Paths generation..."
    path_dijkstra = graph.best_path(node1_pub, node2_pub,amount)
    #Set cut_off for all path exploration
    offset = 1 # Add possible nodes to the path returned by the best_path algorithm
    route_length = len(path_dijkstra)+offset
    paths = get_all_paths(node1_pub, node2_pub, route_length)
    print "Number of paths found for defined route_length", len(paths)
    
    print ">>> [3/4] Fees computing..."
    # Get fees and compare    
    total_fees_dijkstra = get_route_fees(path_dijkstra, amount)
    print "Total fees using best path = ", total_fees_dijkstra
    lowest_fees = get_route_fees(paths[0], amount)
    cheapest_path = [paths[0]]
    for i in range(1,len(paths)):
        fees = get_route_fees(paths[i], amount)
        if (fees < lowest_fees):
            lowest_fees = fees
            cheapest_path = [paths[i]]
        elif (fees == lowest_fees):
            cheapest_path.append(paths[i])
    print "Total fees using all paths finder = ", lowest_fees
    print "Percentage of the amount transferred", 100*lowest_fees/amount
    print "Number of paths with those fees", len(cheapest_path)
    
    print ">>> [4/4] Comparing..."
    if (lowest_fees > total_fees_dijkstra):
        print "Error"
    elif (lowest_fees == total_fees_dijkstra):
        print "OK for fees"
        if path_dijkstra in cheapest_path:
            print "OK path found"
        else:
            print "Error: path not found"
    else:
        print "FAIL | Difference in fees = ", total_fees_dijkstra-lowest_fees

    
def test_manual(amount):
    print ">>> 2 nodes already connected"
    node1_pub = "03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f" #Acinq
    node2_pub = "0388a2cd707ac944a2b0c8adbf67c4a313d24b6dc2ab2baba842f9a9eecf925131" #Estonia
    path = graph.best_path(node1_pub, node2_pub,amount)
    if path==[node1_pub, node2_pub]:
        print "OK"
    else:
        print "FAIL | Number of useless nodes: ", len(path)-2
    
    
def test_path(manual=False, random=True, iter_test=1):
    amount = 100000
    print "Starting comparison..."
    
    if manual:
        print "Test #1: comparison with known paths"
        test_manual(amount)
    
    if random:
        print "Test #2: Generation of all paths from random nodes"
        print "Number of iterations: ", iter_test
        for i in range(iter_test):
            print "--> Iter #", i+1
            test_random(amount)

#%%
    
test_path()