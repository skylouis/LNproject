from src.LN_graph import LN_graph
import requests
from flask import Flask, json,render_template, request


url = 'https://graph.lndexplorer.com/api/graph'
graph = requests.get(url).json()

LN_nodes = graph['nodes']
LN_edges = graph['edges']

graph = LN_graph()

graph.add_nodes(LN_nodes)
graph.add_edges(LN_edges)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    path, cost, LN_nodes_path = graph.best_path(request.form['node1_pub'],
                                 request.form['node2_pub'],
                                 float(request.form['transfered_amount']),
                                 request.form['criteria'])
    return render_template('result.html', path=path, cost=cost)

@app.route('/bestpath/<criteria>/<source_node_pub>/<target_node_pub>/<transfered_amount>')
def bestpath(criteria=None, source_node_pub=None, target_node_pub=None, transfered_amount=None):
    return json.dumps(graph.best_path(source_node_pub,
                                      target_node_pub,
                                      float(transfered_amount),
                                      criteria))
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)