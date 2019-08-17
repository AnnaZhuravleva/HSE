# coding: utf-8

import networkx as nx
import gensim
import matplotlib.pyplot as plt

def main():
    m = 'ruscorpora_mystem_cbow_300_2_2015.bin.gz'
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
    model.init_sims(replace=True)
    words = ['жить_V', 'проживать_V', 'поселяться_V', 'пожить_V', 'обитать_V', 'житься_V', 'поселиться_V',
             'селиться_V']

    G = nx.Graph()
    for i, word in enumerate(words):
        if word in model:
            if i + 1 < len(words):
                for j in range(i+1, len(words)):
                    if words[j] in model:
                        if model.similarity(word, words[j]) > 0.5:
                            # G.add_node(word, label=word)
                            G.add_edge(word, words[j])
        else:
            print(word + ' is not present in the model')

    deg = nx.degree_centrality(G)
    print('центральность узлов')
    for nodeid in sorted(deg, key=deg.get, reverse=False):
        print(nodeid)
    try:
        print('Радиус графа', nx.radius(G))
    except:
        pass
    print('Коэффициент кластеризации:', nx.transitivity(G))

    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='red', node_size=50)
    nx.draw_networkx_edges(G, pos, edge_color='yellow')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='Arial')
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    main()
