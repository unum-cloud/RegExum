import os

from pygraphdb.graph_base import GraphBase
from pygraphdb.helpers import StatsCounter
from pystats.file import StatsFile

from tasks_sampler import TasksSampler


class NetworkXBench(object):

    def local_node_connectivity(self):
        """
        https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.approximation.connectivity.local_node_connectivity.html#networkx.algorithms.approximation.connectivity.local_node_connectivity
        """
        pass

    def average_clustering(self):
        """
        https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.approximation.clustering_coefficient.average_clustering.html#networkx.algorithms.approximation.clustering_coefficient.average_clustering
        """
        pass

        # https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.closeness_centrality.html#networkx.algorithms.centrality.closeness_centrality
        # https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.incremental_closeness_centrality.html#networkx.algorithms.centrality.incremental_closeness_centrality
        # https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.betweenness_centrality_subset.html#networkx.algorithms.centrality.betweenness_centrality_subset

        # https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.group_betweenness_centrality.html#networkx.algorithms.centrality.group_betweenness_centrality
        # https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.group_closeness_centrality.html#networkx.algorithms.centrality.group_closeness_centrality
        # https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.group_degree_centrality.html#networkx.algorithms.centrality.group_degree_centrality
        # https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.harmonic_centrality.html#networkx.algorithms.centrality.harmonic_centrality

        # https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_analysis.pagerank_alg.pagerank_numpy.html#networkx.algorithms.link_analysis.pagerank_alg.pagerank_numpy
        # https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_analysis.hits_alg.hits_numpy.html#networkx.algorithms.link_analysis.hits_alg.hits_numpy

        # https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.dijkstra_path.html#networkx.algorithms.shortest_paths.weighted.dijkstra_path
        # https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.bidirectional_dijkstra.html#networkx.algorithms.shortest_paths.weighted.bidirectional_dijkstra
        # https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.bellman_ford_path.html#networkx.algorithms.shortest_paths.weighted.bellman_ford_path
        # https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.astar.astar_path.html#networkx.algorithms.shortest_paths.astar.astar_path
