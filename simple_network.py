#!/usr/bin/env python
"""Simple example of a graph network with NetworkX"""
# -*- coding: utf-8 -*-
import random
import matplotlib.pyplot as plt
import networkx as nx

with_labels = True


def onclick(event):
    """onclick mouse event for matplotlib"""
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f' % (event.button, event.x, event.y, event.xdata, event.ydata)


def draw_plot(G, pos, with_labels, labels):
    plt.clf()
    nx.draw_networkx(G, pos, with_labels=with_labels, labels=labels, alpha=0.8, node_size=node_sizes, font_size=20, font_family='sans-serif')
    plt.axis("off")
    plt.title("Test graph output")
    plt.show()

def onkey(event):
    """Receive a key-press event, react to 't' to toggle the display of labels"""
    global with_labels
    #print('you pressed', event.key, event.xdata, event.ydata)
    if event.key == "t":
        with_labels = not with_labels
        draw_plot(G, pos, with_labels, labels)
        print "Toggled labels, redrawn"


#def onpick(event):
#    # via http://matplotlib.org/api/backend_bases_api.html#matplotlib.backend_bases.PickEvent
#    thisline = event.artist
#    xdata, ydata = thisline.get_data()
#    ind = event.ind
#    print('on pick line:', zip(xdata[ind], ydata[ind]))


if __name__ == "__main__":
    # build a simple graph that could be circular

    nodes = [0, 1, 2, 3, 4, 5, 6]
    edges = [(2, 3), (4, 5), (5, 6), (4, 6)]
    # programmatically add connections to a central node 0
    for e in range(1, 7):
        edges.append((0, e))

    print edges

    G = nx.Graph()
    for n in nodes:
        G.add_node(n, label=str(n), value=random.random())
    G.add_edges_from(edges)

    # remove nodes that are poorly connected
    nodes_with_few_edges = [nd for nd in G.nodes() if len(G.neighbors(nd)) < 2]
    print "We had these nodes:", G.nodes()
    G.remove_nodes_from(nodes_with_few_edges)
    print "After filtering we have these nodes:", G.nodes()

    prog = "neato"  # neato is default layout engine in GraphViz
    # create a set of positions (x,y coords) as a dict against the node names
    pos = nx.graphviz_layout(G, prog=prog, root=None, args="")

    # dictionary comprehension for labels
    labels = {node: G.node[node]['label'] for node in G.nodes()}
    # 100-500 make for good sizes
    node_sizes = [data['value'] * 500 for node, data in G.nodes(data=True)]
    fig = plt.figure()
    draw_plot(G, pos, with_labels, labels)

    # make the plot go full-screen (works on TkAGG)
    # plt.get_backend() == 'TkAgg'
    #mng = plt.get_current_fig_manager()
    #mng.full_screen_toggle()
    # make the maximised plot tidy up to use more of the plot area
    plt.tight_layout()

    # attach a mouse-click detector
    #cid = fig.canvas.mpl_connect('button_press_event', onclick)
    cid = fig.canvas.mpl_connect('key_press_event', onkey)

    # TODO figure out how to attach an artist to the nodes that I've drawn
    #cid2 = fig.canvas.mpl_connect('pick_event', onpick)
    # fig.axes[0].axes.texts  # seems to contain the text labels that we've
    # drawn
    # fig.axes[0].add_artist  # might let me add an artist

    # plt.close()  # close the figure when we're done with it
