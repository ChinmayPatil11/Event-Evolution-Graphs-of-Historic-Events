import dash
import networkx as nx
from dash import html
from dash import dcc
from pattern_matcher import pattern_matcher
from dash.dependencies import Input, Output, State
import dash_cytoscape as cyto
from dash import dash_table
from network import create_graph, create_dash_graph
from data_cleaner import clean_df
import pandas as pd
import os

path = '/data'
csv_files = []
for file in os.listdir(os.curdir + path):
    if file.endswith('.csv'):
        csv_files.append(file)

for file in csv_files:
    df = pd.read_csv('data/'+file)
    df = pattern_matcher(df)
    df = clean_df(df)
    G = create_graph(df)

default_stylesheet = [{
                'selector': 'node',
                'style': {
                    'label': 'data(id)'
                }
            },
            {'selector': 'edge',
                'style': {
                    'target-arrow-shape': 'triangle',
                    'label': 'data(relation)'
                }}]

elements = create_dash_graph(G)
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([html.H1('A graph of events in history', style={'textAlign': 'center'}),
    html.Div([
    html.Div(style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top'},
             children=[dcc.RangeSlider(id='slider-input', min=1600, max=1900, step=10, value=[1600, 1900],
                                       marks={
                                           1600: '1600',
                                           1650: '1650',
                                           1700: '1700',
                                           1750: '1750',
                                           1800: '1800',
                                           1850: '1850',
                                           1900: '1900'
                                       }),
                       cyto.Cytoscape(id='cytoscape-graph',
                                      layout={'name': 'random'},
                                      style={'width': '100%', 'height': '600px', 'border': 'thin lightgrey solid'},
                                      elements=elements,
                                      stylesheet=default_stylesheet)]
             ),
    html.Div(style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top', 'border': 'thin lightgrey solid'},
             children=[html.Div([html.H4('Selected Node data', style={'textAlign': 'center'}),
                        dash_table.DataTable(id='dash-table',
                                             columns=[{'name': i, 'id': i, 'selectable': True} for i in ['source', 'relation', 'target']],
                                             style_cell={'textAlign': 'center'}
                                            )]),
                       html.Div([html.H4('Node Check'),
                                 html.P('Check if a node is present in the network.'
                                        ' If present it will highlight the nodes, otherwise the node is absent'),
                                 dcc.Input(id='input-node', type='text', n_submit=0),
                                 html.Div(id='node-present')])
                       ])
])])


@app.callback(
    Output('cytoscape-graph', 'elements'),
    Input('slider-input', 'value')
)
def update_cytoscape(value):
    if value == [1600, 1900]:
        return elements
    else:
        lowrange, highrange = min(value), max(value)
        nodes = []
        edges = []
        for node in G.nodes:
            if node.isdigit():
                if (int(node) > lowrange) and (int(node) < highrange):
                    nodes.append(node)
        out_nodes = []
        for node in nodes:
            for n in G.out_edges(node):
                if n[1] not in out_nodes:
                    out_nodes.append(n[1])
        nodes = nodes + out_nodes
        for onode in out_nodes:
            for i in G.out_edges(onode):
                if i not in nodes:
                    nodes.append(i[1])
        for edge in G.edges(data=True):
            if edge[0] in nodes or edge[1] in nodes:
                edges.append(edge)
        new_G = nx.MultiDiGraph()
        new_G.add_nodes_from(nodes)
        new_G.add_edges_from(edges)
        new_G_list = create_dash_graph(new_G)
        return new_G_list

@app.callback(
    Output('dash-table', 'data'),
    Input('cytoscape-graph', 'tapNode')
)
def displaynode(data):
    sources = []
    relations = []
    targets = []
    if data:
        for node in data['edgesData']:
            if 'relation' in node.keys():
                sources.append(node['source'])
                relations.append(node['relation'])
                targets.append(node['target'])
            else:
                sources.append(node['source'])
                relations.append('-')
                targets.append(node['target'])
    df = pd.DataFrame({'source': sources, 'relation': relations, 'target': targets})
    return df.to_dict('records')

@app.callback(
    Output('cytoscape-graph', 'stylesheet'),
    Input('cytoscape-graph', 'tapNode'),
    Input('input-node', 'n_submit'),
    State('input-node', 'value')
)
def update_node(node, n_submit, value):
    if not node and not value:
        return default_stylesheet
    ctx = dash.callback_context
    if not ctx:
        pass
    else:
        ip = ctx.triggered[0]['prop_id'].split('.')[0]

    if ip == 'cytoscape-graph':
        stylesheet = [{
            "selector": 'node',
            'style': {
                'opacity': 0.3
            }
        }, {
            'selector': 'edge',
            'style': {
                'opacity': 0.2,
                "curve-style": "bezier"
            }
        }, {
            "selector": 'node[id = "{}"]'.format(node['data']['id']),
            "style": {
                'background-color': '#B10DC9',
                "border-color": "purple",
                "border-width": 2,
                "border-opacity": 1,
                "opacity": 1,

                "label": "data(label)",
                "color": "#B10DC9",
                "text-opacity": 1,
                "font-size": 12,
                'z-index': 9999
            }
        }]

        for edge in node['edgesData']:
            if edge['source'] == node['data']['id']:
                stylesheet.append({
                    "selector": 'node[id = "{}"]'.format(edge['target']),
                    "style": {
                        'opacity': 0.9,
                        'background-color': 'red',
                        'label': 'data(id)'
                    }
                })
                stylesheet.append({
                    "selector": 'edge[id= "{}"]'.format(edge['id']),
                    "style": {
                        "mid-target-arrow-shape": "vee",
                        'opacity': 0.9,
                        'z-index': 5000,
                        'label': 'data(relation)',
                        'line-color': 'red'
                    }
                })

            if edge['target'] == node['data']['id']:
                stylesheet.append({
                    "selector": 'node[id = "{}"]'.format(edge['source']),
                    "style": {
                        'opacity': 0.9,
                        'z-index': 9999,
                        'background-color': 'blue',
                        'label': 'data(id)'
                    }
                })
                stylesheet.append({
                    "selector": 'edge[id= "{}"]'.format(edge['id']),
                    "style": {
                        "mid-target-arrow-shape": "vee",
                        'opacity': 1,
                        'z-index': 5000,
                        'label': 'data(relation)',
                        'line-color': 'blue'
                    }
                })

        return stylesheet

    if ip == 'input-node':
        nodelist, nodeidlist = [], []
        stylesheet = [{
            "selector": 'node',
            'style': {
                'opacity': 0.3
            }
        }, {
            'selector': 'edge',
            'style': {
                'opacity': 0.2,
                "curve-style": "bezier"
            }
        }]
        for node in elements:
            if 'label' in node['data'].keys():
                if value in node['data']['label']:
                    nodelist.append(node)
                    nodeidlist.append(node['data']['id'])

        for node in nodelist:
            stylesheet.append({
                "selector": 'node[id = "{}"]'.format(node['data']['id']),
                "style": {
                    'background-color': '#B10DC9',
                    "border-color": "purple",
                    "border-width": 2,
                    "border-opacity": 1,
                    "opacity": 1,

                    "label": "data(label)",
                    "color": "#B10DC9",
                    "text-opacity": 1,
                    "font-size": 12,
                    'z-index': 9999
                }
            })

        for edge in elements:
            if 'source' in edge['data'].keys():
                if edge['data']['source'] in nodeidlist:
                    stylesheet.append({
                        "selector": 'node[id = "{}"]'.format(edge['data']['target']),
                        "style": {
                            'opacity': 0.9,
                            'background-color': 'red',
                            'label': 'data(id)'
                        }
                    })
                    stylesheet.append({
                        "selector": 'edge[id= "{}"]'.format(edge['data']['id']),
                        "style": {
                            "mid-target-arrow-shape": "vee",
                            'opacity': 0.9,
                            'z-index': 5000,
                            'label': 'data(relation)',
                            'line-color': 'red'
                        }
                    })
    
                if edge['data']['target'] in nodeidlist:
                    stylesheet.append({
                        "selector": 'node[id = "{}"]'.format(edge['data']['source']),
                        "style": {
                            'opacity': 0.9,
                            'z-index': 9999,
                            'background-color': 'blue',
                            'label': 'data(id)'
                        }
                    })
                    stylesheet.append({
                        "selector": 'edge[id= "{}"]'.format(edge['data']['id']),
                        "style": {
                            "mid-target-arrow-shape": "vee",
                            'opacity': 1,
                            'z-index': 5000,
                            'label': 'data(relation)',
                            'line-color': 'blue'
                        }
                    })

        return stylesheet


@app.callback(
    Output('node-present', 'children'),
    Input('input-node', 'n_submit'),
    State('input-node', 'value')
)
def show_node(n_submit, value):
    present = False
    if value:
        lst = []
        for node in elements:
            if 'label' in node['data'].keys():
                if value in node['data']['label']:
                    present = True
                    lst.append(node['data']['label'])
        if present:
            return [html.Li(i) for i in lst]
        else:
            return 'node absent'


if __name__ == '__main__':
    app.run_server(debug=True)