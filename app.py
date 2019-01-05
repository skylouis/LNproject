from src.LN_graph import LN_graph
import requests
from flask import Flask, json

#%%
url = 'https://graph.lndexplorer.com/api/graph'
graph = requests.get(url).json()

LN_nodes = graph['nodes']
LN_edges = graph['edges']

graph = LN_graph()

graph.add_nodes(LN_nodes)
graph.add_edges(LN_edges)
#%%
app = Flask(__name__)
@app.route('/bestpath/<criteria>/<source_node_pub>/<target_node_pub>/<transfered_amount>')
def bestpath(criteria=None, source_node_pub=None, target_node_pub=None, transfered_amount=None):
    return json.dumps(graph.best_path(source_node_pub,
                                      target_node_pub,
                                      float(transfered_amount),
                                      criteria))