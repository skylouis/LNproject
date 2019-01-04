import networkx as nx
import numpy as np


def Dijkstra(nx_graph, source_mode_id, weight_function, amount_transfered):
    
    mode_ids = []
    dist = dict()
    prev = dict()
    
    for mode_id in nx_graph.nodes:
        dist[mode_id] = np.inf
        prev[mode_id] = np.nan
        mode_ids.append(mode_id)
    
    dist[source_mode_id] = 0
    
    while len(mode_ids) > 0:
        min_dist_mode_id = mode_ids[np.argmin([dist[mode_id] for node_id in mode_ids])]
        mode_ids.remove(min_dist_mode_id)
        
        for neighbor_node_id in nx_graph.neighbors(min_dist_mode_id):
            alt = dist[min_dist_mode_id] + weight_function(
                    min_dist_mode_id,
                    neighbor_node_id,
                    amount_transfered + dist[min_dist_mode_id])
            if alt < dist[neighbor_node_id]:
                dist[neighbor_node_id] = alt
                for node_id, value in prev.iteritems():
                    if value == neighbor_node_id:
                        dist[value] = alt + weight_function(
                            min_dist_mode_id,
                            neighbor_node_id,
                            amount_transfered + dist[min_dist_mode_id])
                        
                    
                prev[neighbor_node_id] = min_dist_mode_id
    return dist, prev

