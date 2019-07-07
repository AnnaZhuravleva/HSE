
# coding: utf-8

# In[4]:


import networkx as nx
import sys
import gensim, logging
import matplotlib.pyplot as plt

%time model = logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

m = 'ruscorpora_mystem_cbow_300_2_2015.bin.gz'
if m.endswith('.vec.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
elif m.endswith('.bin.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
else:
    model = gensim.models.KeyedVectors.load(m)
model.init_sims(replace=True)
words = ['жить_VERB','проживатьть_VERB', 'поселяться_VERB', 'пожить_VERB','прожить_VERB','обитать_VERB', 'житься_VERB', 'поселиться_VERB', 'селиться_VERB']

G = nx.Graph()
for word in words:
    G.add_node(word, label=word)
for i, word in enumerate(words):
    if word in model:
        if i + 1 < len(words):
            for j in range (i+1, len(words)):
                if words[j] in model:
                    if model.similarity(word, words[j])> 0.5:
                        G.add_edge(word, words[j])
    else:
        print(word + ' is not present in the model')


deg = nx.degree_centrality(G)
print('центральность узлов')
for nodeid in sorted(deg, key=deg.get, reverse=True):
    print(nodeid)
print('Радиус графа')
print(nx.radius(G))
print('Коэффициент кластеризации:')
print(nx.transitivity(G))


pos=nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_color='red', node_size=50)
nx.draw_networkx_edges(G, pos, edge_color='yellow')
nx.draw_networkx_labels(G, pos, font_size=10, font_family='Arial')
plt.axis('off')
plt.show()

