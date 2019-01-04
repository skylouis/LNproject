import networkx as nx

class LN_graph(object):
    def __init__(self):
        self.nx_graph = nx.DiGraph()
    
    def add_nodes(self, LN_nodes):
        """add nodes from the LN nodes class"""
        for LN_node in LN_nodes:
            self.nx_graph.add_node(LN_node.pub_key,
                                   last_update=LN_node.last_update,
                                   )
        return
    
    def add_edges(self, LN_edges):
        """add edges from the LN edges class"""
        for LN_edge in LN_edges:
            self.nx_graph.add_node(LN_edge.node1_pub,
                                   LN_edge.node2_pub,
                                   channel_id=LN_edge.channel_id,
                                   last_update=LN_edge.last_update,
                                   capacity=LN_edge.capacity,
                                   time_lock_delta=LN_edge.node1_policy.time_lock_delta,
                                   min_htlc=LN_edge.node1_policy.min_htlc,
                                   fee_base_msat=LN_edge.node1_policy.fee_base_msat,
                                   fee_rate_milli_msat=LN_edge.node1_policy.fee_rate_milli_msat,
                                   disabled=LN_edge.node1_policy.disabled,
                                   )
            self.nx_graph.add_node(LN_edge.node2_pub,
                                   LN_edge.node1_pub,
                                   channel_id=LN_edge.channel_id,
                                   last_update=LN_edge.last_update,
                                   capacity=LN_edge.capacity,
                                   time_lock_delta=LN_edge.node2_policy.time_lock_delta,
                                   min_htlc=LN_edge.node2_policy.min_htlc,
                                   fee_base_msat=LN_edge.node2_policy.fee_base_msat,
                                   fee_rate_milli_msat=LN_edge.node2_policy.fee_rate_milli_msat,
                                   disabled=LN_edge.node2_policy.disabled,
                                   )
    
    def capacity_limitat_subgraph(self, transfered_amount):
        """ """
        return 
    
    def neighbors(self, node_pub):
        """neighbors of the node """
        return self.nx_graph.neighbors(node_pub)
    
    def capacity(self, node1_pub, node2_pub):
        return self.nx_graph[node1_pub, node2_pub]['capacity']
    
    def fee_tranfert(self, node1_pub, node2_pub, transfered_amount):
        """lambda function to compute the fee transfert of the amount transfert"""
        fee_base_msat = self.nx_graph[node1_pub, node2_pub]['fee_base_msat']
        fee_rate_milli_msat = self.nx_graph[node1_pub, node2_pub]['fee_rate_milli_msat']
        return  fee_base_msat + 1. * fee_rate_milli_msat * transfered_amount / 1000
    
    def time_locks(self, node1_pub, node2_pub):
        return self.nx_graph[node1_pub, node2_pub]['time_locks']
    
    
    
