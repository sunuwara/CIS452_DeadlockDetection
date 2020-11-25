"""
Title: CIS 452 Project 2: Resource Manager Single Instance Deadlock Detection
Author: Aron Sunuwar
Date: November 24, 2020

Description: This is the class that handles the graphical display of the resource
             allocation graph.
"""

import matplotlib.pyplot as plt
import networkx as nx


class GraphGUI:
    """ Class to handle the graphical display of the resource allocation graph """

    def __init__(self, diGraph):
        self.nx = nx
        self.plt = plt
        self.pltTitle = ""
        self.rag = diGraph
        self.pNodes = list()
        self.rNodes = list()
        self.p2rEdges = list()
        self.r2pEdges = list()

    def initialize(self, title):
        """ Separate process and resource nodes for use and initialize variables """

        for node in self.rag:
            if node[0] == "P":
                self.pNodes.append(node)
            if node[0] == "R":
                self.rNodes.append(node)

        self.pltTitle = title
        self.plt.figure(figsize=(5, 5))

    def drawNodes(self):
        """ Draw each of the nodes with configurations """
        labels = {}
        pos = self.nx.circular_layout(self.rag)

        for node in self.rag:
            labels[node] = node

        self.nx.draw_networkx_nodes(self.rag, pos,
                                    nodelist=self.pNodes,
                                    node_size=500,
                                    node_color="dodgerblue",
                                    node_shape="o",
                                    alpha=0.8,
                                    edgecolors="black",
                                    label="Process")
        self.nx.draw_networkx_nodes(self.rag, pos,
                                    nodelist=self.rNodes,
                                    node_size=500,
                                    node_color="red",
                                    node_shape="s",
                                    alpha=0.8,
                                    edgecolors="black",
                                    label="Resource")

        self.nx.draw_networkx_labels(self.rag, pos, labels=labels)

    def drawEdges(self):
        """ Draw each of the edges with configurations """
        pos = self.nx.circular_layout(self.rag)
        self.p2rEdges.clear()
        self.r2pEdges.clear()

        for edge in self.rag.edges():
            if edge[0][0] == 'P':
                self.p2rEdges.append(edge)
            else:
                self.r2pEdges.append(edge)

        self.nx.draw_networkx_edges(self.rag, pos,
                                    edgelist=self.p2rEdges,
                                    width=3,
                                    edge_color="dodgerblue",
                                    alpha=0.8,
                                    arrows=True,
                                    arrowsize=10)
        self.nx.draw_networkx_edges(self.rag, pos,
                                    edgelist=self.r2pEdges,
                                    width=3,
                                    edge_color="red",
                                    alpha=0.8,
                                    arrows=True,
                                    arrowsize=10)

    def display(self, message):
        """ Plot out the graph and display """
        self.plt.clf()

        self.drawNodes()
        self.drawEdges()

        self.plt.title(message)
        self.plt.show()

    def close(self):
        """ Close out graph plot """
        self.plt.close()
