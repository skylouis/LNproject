import networkx as nx
import numpy as np
from shortest_path_algo import dijkstra

class LN_graph(object):
    def __init__(self):
        self.nx_graph = nx.DiGraph()

    def add_nodes(self, LN_nodes):
        """add nodes from the LN nodes class"""
        for LN_node in LN_nodes:
            if 'geo_info' in LN_node.keys():
                geo_info = LN_node['geo_info']
            else:
                geo_info = np.nan

            self.nx_graph.add_node(LN_node['pub_key'],
                                   last_update=LN_node['last_update'],
                                   geo_info=geo_info,   
                                   alias=LN_node['alias'],
                                   color=LN_node['color']
                                   )
        return

    def add_edges(self, LN_edges):
        """add edges from the LN edges class"""
        for LN_edge in LN_edges:
            if LN_edge['node1_policy'] and LN_edge['node2_policy']:
                self.nx_graph.add_edge(LN_edge['node1_pub'],
                                       LN_edge['node2_pub'],
                                       channel_id=LN_edge['channel_id'],
                                       last_update=LN_edge['last_update'],
                                       capacity=LN_edge['capacity'],
                                       time_lock_delta=LN_edge['node1_policy']['time_lock_delta'],
                                       min_htlc=LN_edge['node1_policy']['min_htlc'],
                                       fee_base_msat=LN_edge['node1_policy']['fee_base_msat'],
                                       fee_rate_milli_msat=LN_edge['node1_policy']['fee_rate_milli_msat'],
                                       disabled=LN_edge['node1_policy']['disabled'],
                                       )
                self.nx_graph.add_edge(LN_edge['node2_pub'],
                                       LN_edge['node1_pub'],
                                       channel_id=LN_edge['channel_id'],
                                       last_update=LN_edge['last_update'],
                                       capacity=LN_edge['capacity'],
                                       time_lock_delta=LN_edge['node2_policy']['time_lock_delta'],
                                       min_htlc=LN_edge['node2_policy']['min_htlc'],
                                       fee_base_msat=LN_edge['node2_policy']['fee_base_msat'],
                                       fee_rate_milli_msat=LN_edge['node2_policy']['fee_rate_milli_msat'],
                                       disabled=LN_edge['node2_policy']['disabled'],
                                       )

    def neighbors(self, node_pub):
        """neighbors of the node """
        return self.nx_graph.neighbors(node_pub)

    def capacity(self, node1_pub, node2_pub):
        return self.nx_graph[node1_pub, node2_pub]['capacity']

    def fee_tranfert(self, node1_pub, node2_pub, transfered_amount):
        """lambda function to compute the fee transfert of the amount transfert"""
        fee_base_msat = float(self.nx_graph[node1_pub][node2_pub]['fee_base_msat'])
        fee_rate_milli_msat = float(self.nx_graph[node1_pub][node2_pub]['fee_rate_milli_msat'])
        return  fee_base_msat + (1. * fee_rate_milli_msat / 1000) * transfered_amount
    
    def get_route_fees(self, path, amount):
        total_fees = 0
        new_amount = amount
        for i in reversed(range(1,len(path))):
            fees = self.fee_tranfert(path[i-1],path[i],new_amount)
            total_fees += fees
            new_amount += fees
        return total_fees

    def time_locks(self, node1_pub, node2_pub):
        return self.nx_graph[node1_pub, node2_pub]['time_locks']

    def best_path(self, node1_pub, node2_pub, transfered_amount, cost_method='fee', method='dijkstra'):
        if cost_method=='fee':
            cost_function = lambda node1_pub, node2_pub, transfered_amount: self.fee_tranfert(node2_pub, node1_pub, transfered_amount)
        elif cost_method=='node':
            cost_function = lambda node1_pub, node2_pub, transfered_amount: 1

        if method=='dijkstra':
            algorithm = dijkstra

        path, cost = algorithm(self.nx_graph,
                         source_node_id=node2_pub,
                         target_node_id=node1_pub,
                         weight_function=cost_function,
                         amount_transfered=transfered_amount)
        LN_nodes_path = []
        for pub_key in path:
            LN_node = self.nx_graph.nodes[pub_key]
            LN_node['pub_key'] = pub_key
            LN_nodes_path.append(LN_node)
            
        if cost_method=='node':
            cost = self.get_route_fees(path, transfered_amount)            

        return path, cost, LN_nodes_path

    def has_node(self, node_pub):
        """Returns whether a given node public key is in the lightning network"""
        return self.nx_graph.has_node(node_pub)
