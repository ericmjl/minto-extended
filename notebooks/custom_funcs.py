from copy import copy, deepcopy
import pandas as pd


def print_graph_data(G):
    print('Graph has {0} nodes.'.format(len(G.nodes())))
    print('Graph has {0} edges.'.format(len(G.edges())))


def node_metadata_as_dataframe(G):
    data = list()
    for n, d in G.nodes(data=True):
        d = copy(d)
        d['strain_name'] = n
        data.append(d)
    df = pd.DataFrame(data)
    return df


def edge_metadata_as_dataframe(G):
    data = list()
    for sc, sk, d in G.edges(data=True):
        datum = deepcopy(d)

        datum['source'] = sc
        datum['sink'] = sk

        # Split out the edge "segments" metadata.
        for k, v in d.items():
            if k == 'segments':
                for segnum, pwi in v.items():
                    datum['segment {0} pwi'.format(segnum)] = pwi

        # Add in sink metadata
        sc_d = G.node[sc]
        for k, v in sc_d.items():
            datum['source_{0}'.format(k)] = v

        sk_d = G.node[sk]
        for k, v in sk_d.items():
            datum['sink_{0}'.format(k)] = v

        data.append(datum)
    df = pd.DataFrame(data)
    return df
