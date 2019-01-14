import networkx as nx
import numpy as np


def dijkstra(nx_graph, source_node_id, target_node_id, weight_function, amount_transfered):

    node_ids = []
    dist = dict()
    prev = dict()

    for node_id in nx_graph.nodes:
        dist[node_id] = np.inf
        prev[node_id] = np.nan
        node_ids.append(node_id)

    dist[source_node_id] = 0

    while len(node_ids) > 0:
        min_dist_node_id = node_ids[np.argmin([dist[node_id] for node_id in node_ids])]
        node_ids.remove(min_dist_node_id)
        if not np.isinf(dist[min_dist_node_id]):
            for neighbor_node_id in nx_graph.neighbors(min_dist_node_id):
                if float(nx_graph[min_dist_node_id][neighbor_node_id]['capacity']) > (amount_transfered + dist[min_dist_node_id])/1e3:
                    alt = dist[min_dist_node_id] + weight_function(
                            min_dist_node_id,
                            neighbor_node_id,
                            amount_transfered + dist[min_dist_node_id])

                    if alt < dist[neighbor_node_id]:
                        dist[neighbor_node_id] = alt
                        for node_id, value in prev.iteritems():
                            if value == neighbor_node_id:
                                dist[value] = alt + weight_function(
                                    min_dist_node_id,
                                    neighbor_node_id,
                                    amount_transfered + dist[min_dist_node_id])

                        prev[neighbor_node_id] = min_dist_node_id

    path = [target_node_id]
    while path[-1] != source_node_id:
        path.append(prev[path[-1]])

    return path, dist[target_node_id]
