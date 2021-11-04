import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go

G = nx.MultiDiGraph()


def create_graph(df):
    source = df['subject'].tolist()
    target = df['object'].tolist()
    edge = df['verb'].tolist()
    years = df['year from'].tolist()
    for i in range(len(source)):
        triple = (years[i], source[i], edge[i], target[i])
        if [''] not in triple:
            G.add_node(triple[0])
            G.add_node(triple[1][0])
            G.add_node(triple[3][0])
            G.add_edge(triple[0], triple[1][0], relation=None)
            G.add_edge(triple[1][0], triple[3][0], relation=triple[2][0])

    for i in range(1600,1900):
        if str(i) in G.nodes() and str(i+1) in G.nodes():
            G.add_edge(str(i),str(i+1))
    #plt.figure(figsize=(20, 20))
    #nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
    #        node_size=500, node_color='seagreen', alpha=0.9,
    #        labels={node: node for node in G.nodes()})
    return G


def create_dash_graph(G):
    pos = nx.spring_layout(G)
    cy = nx.readwrite.cytoscape_data(G)
    for node in cy['elements']['nodes']:
        for k, v in node.items():
            v['label'] = v.pop('value')
    for n, p in zip(cy['elements']['nodes'],pos.values()):
        n['pos'] = {'x':p[0],'y':p[1]}
    for edge in cy['elements']['edges']:
        edge['data']['id'] = edge['data']['source'] + edge['data']['target']
    element_ls = cy['elements']['nodes'] + cy['elements']['edges']
    return element_ls