import networkx as nx
G = nx.Graph()
G.add_node(1)
G.add_nodes_from([2,3])
G.add_nodes_from(["u","v"])
G.nodes()
G.add_edge(1,2)
G.add_edge("u","v")
G.add_edges_from([(1,3),(1,4),(1,5),(1,6)])
G.add_edge("u","w")
#G.remove_edge(2)
G.number_of_edges()
G.number_of_nodes()

G = nx.karate_club_graph()
import matplotlib.pyplot as plt
nx.draw(G, with_labels=True, node_color="lightblue",edge_color="gray")
plt.savefig("Karate_graph.pdf")
from scipy.stats import bernoulli
def er_graph(N,p):
    """generate an ER graph."""
    G = nx.Graph()
    G.add_nodes_from(range(N))
    for node1 in G.nodes():
        for node2 in G.nodes():
            if node1 < node2 and bernoulli.rvs(p=p) == True:
                G.add_edge(node1, node2)
    return G

nx.draw(er_graph(50,0.08),node_size=40,node_color="gray")
plt.savefig("er1.pdf")


def plot_degree_distribution(G):
    degree_sequence = [d for n, d in G.degree()]
    plt.hist(degree_sequence, histtype="step")
    plt.xlabel("Degree $k$")
    plt.ylabel("$P(k)$")
    plt.title("Degree Distribution")

G1 = er_graph(500, 0.08)
plot_degree_distribution(G1)
plt.savefig("hist1.pdf")
G2 = er_graph(500, 0.08)
plot_degree_distribution(G2)
plt.savefig("hist2.pdf")
G3 = er_graph(500, 0.08)
plot_degree_distribution(G3)
plt.savefig("hist3.pdf")

import numpy as np
A1 = np.loadtxt("C:\\Users\\User\Downloads\\adj_allVillageRelationships_vilno_1.csv",delimiter=",")
A2 = np.loadtxt("C:\\Users\\User\Downloads\\adj_allVillageRelationships_vilno_2.csv",delimiter=",")

G1 = nx.to_networkx_graph(A1)
G2 = nx.to_networkx_graph(A2)

def basic_net_stats(G):
    print("Number of nodes: %d" % G.number_of_nodes())
    print("Number of edges: %d" % G.number_of_edges())
    degree_sequence = [d for n, d in G.degree()]
    print("Average degree: %.2f" % np.mean(degree_sequence))

plot_degree_distribution(G1)
plot_degree_distribution(G2)
plt.hist("village_hist.pdf")
