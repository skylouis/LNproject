import json
from src.LN_graph import LN_graph

graph = json.load(file('LN_snapshot/graph.json','rw'))

LN_nodes = graph['nodes']
LN_edges = graph['edges']

graph = LN_graph()

graph.add_nodes(LN_nodes)
graph.add_edges(LN_edges)
#%%
print graph.best_path('022fbf66d0c695894bd5de86e35764f4890fcdf4ef577b3f8bc25efd55b4f220e3',
                      '02f304f0ed1dd6ae7b8677025e40c9254b3b9d77a44718f21aa3e3322552af7562',
                      100000)