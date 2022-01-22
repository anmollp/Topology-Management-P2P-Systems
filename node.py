import heapq
import random

from TwoDPoint import TwoDPoint
from utils import Utils


class Node:
    """
    Node class that represents a single node entity
    """
    def __init__(self, node_id, x_co_ordinate, y_co_ordinate):
        """
        Initializer
        :param node_id: identifier for a node
        :param x_co_ordinate: x co-ordinate
        :param y_co_ordinate: y co-ordinate
        """
        self.id = node_id
        self.position = TwoDPoint(x_co_ordinate, y_co_ordinate)
        self.r_g_b = []
        self.color = ""
        self.l_distance = 0
        self.a_distance = 0
        self.b_distance = 0
        self.neighbors = []

    def select_random_neighbor(self, k):
        """
        choose a random neighbor from neighbor's list
        :param k: number of neighbors
        :return: a random neighbor
        """
        return self.neighbors[random.randrange(0, k)]

    def get_identifiers(self):
        """
        get neighbors of self
        """
        return self.neighbors

    def select_k_nearest_neighbors(self, nodes, k):
        """
        min heap based finding k nearest neighbors based on the distance criteria as provided in the assignment
        :param nodes: set of all nodes
        :param k: the number of neighbors to choose
        :return: k nearest neighbors
        """
        distance_pq = []
        num_nodes = len(nodes)

        for i in range(num_nodes):
            point_A = (self.l_distance, self.a_distance, self.b_distance)
            point_B = (nodes[i].l_distance, nodes[i].a_distance, nodes[i].b_distance)
            dist = Utils.compute_distance(point_A, point_B)
            heapq.heappush(distance_pq, (dist, nodes[i].id, nodes[i]))

        k_nearest_neighbors = []
        while k:
            _, _, node = heapq.heappop(distance_pq)
            k_nearest_neighbors.append(node)
            k -= 1

        return k_nearest_neighbors

    def update_neighbors(self, identifier_list, k):
        """
        form a new set of neighbors based on merger of incoming neighbor set from sender and self neighbors list
        :param identifier_list:
        :param k: the number of neighbors to choose
        :return: None
        """
        merged_list = set(self.neighbors).union(set(identifier_list))

        if self in merged_list:
            merged_list.remove(self)

        self.neighbors = self.select_k_nearest_neighbors(list(merged_list), k)


    