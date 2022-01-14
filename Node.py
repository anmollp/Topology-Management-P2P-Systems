import heapq
import random

from TwoDPoint import TwoDPoint
from utils import Utils


class Node:
    def __init__(self, node_id, x_co_ordinate, y_co_ordinate):
        self.id = node_id
        self.position = TwoDPoint(x_co_ordinate, y_co_ordinate)
        self.r_g_b = []
        self.color = ""
        self.l_distance = 0
        self.a_distance = 0
        self.b_distance = 0
        self.neighbors = []

    def select_random_neighbor(self, k):
        return self.neighbors[random.randrange(0, k)]

    def get_identifiers(self):
        """
        send identifiers of self and neighbors to node
        """
        return self.neighbors

    def select_k_nearest_neighbors(self, nodes, k):
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
        merged_list = set(identifier_list).union(set(self.neighbors))
        if self in merged_list:
            merged_list.remove(self)
        self.neighbors = self.select_k_nearest_neighbors(list(merged_list), k)


    