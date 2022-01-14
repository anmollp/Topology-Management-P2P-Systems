import heapq
import math
import matplotlib.pyplot as plt
import random
import numpy as np

from Node import Node
from utils import Utils


class Topology:
    def __init__(self, topology_type, num_nodes, k, epochs, m, radii):
        self.topology_type = topology_type
        self.num_nodes = num_nodes
        self.epochs = epochs
        self.nodes = []
        self.k = k
        self.m = m
        self.radii = radii
        self.build_nodes()
        self.initialise_network_of_nodes()
        self.evolve_network()

    def get_color_count(self, groups):
        """
        :return: a map of color counts
        """
        red_count, green_count, blue_count = [self.num_nodes // groups + (1 if x < self.num_nodes % groups else 0) for x
                                              in
                                              range(groups)]
        return red_count, green_count, blue_count

    def get_nodes_color_randomized(self, groups, points_set: set):
        red, green, blue = self.get_color_count(groups)
        points_colored = []

        for i in range(red):
            red_point = random.choice(tuple(points_set))
            r, g, b, color = Utils.get_red_color()
            points_colored.append((red_point, r, g, b, color))
            points_set.remove(red_point)

        for i in range(green):
            green_point = random.choice(tuple(points_set))
            r, g, b, color = Utils.get_green_color()
            points_colored.append((green_point, r, g, b, color))
            points_set.remove(green_point)

        for i in range(blue):
            blue_point = random.choice(tuple(points_set))
            r, g, b, color = Utils.get_blue_color()
            points_colored.append((blue_point, r, g, b, color))
            points_set.remove(blue_point)

        return points_colored

    def select_k_neighbors(self, node):
        distance_pq = []

        for i in range(self.num_nodes):
            if node.id == self.nodes[i].id:
                continue
            point_A = (node.l_distance, node.a_distance, node.b_distance)
            point_B = (self.nodes[i].l_distance, self.nodes[i].a_distance, self.nodes[i].b_distance)
            dist = Utils.compute_distance(point_A, point_B)
            heapq.heappush(distance_pq, (dist, self.nodes[i].id, self.nodes[i]))

        k_nearest_neighbors = []
        top_k = self.k
        while top_k:
            _, _, node = heapq.heappop(distance_pq)
            k_nearest_neighbors.append(node)
            top_k -= 1

        return k_nearest_neighbors

    def build_nodes(self):
        # theta = [math.pi / 2 - ((i - 1) * (math.pi / (self.num_nodes - 2))) for i in range(self.num_nodes)]
        theta = [2 * math.pi / self.num_nodes * i for i in range(self.num_nodes)]
        co_ordinates = set((math.cos(t), math.sin(t)) for t in theta)

        colored_nodes = self.get_nodes_color_randomized(3, co_ordinates)
        points, r, g, b, color = zip(*colored_nodes)

        X, Y, Z = Utils.transform_rgb_to_xyz(r, g, b)
        l, a, b = Utils.transform_xyz_to_cie_l_ab(X, Y, Z)

        for i in range(0, self.num_nodes):
            node = Node(i, points[i][0], points[i][1])
            node.l_distance = l[i]
            node.a_distance = a[i]
            node.b_distance = b[i]
            node.r_g_b = [r[i], g[i], b[i]]
            node.color = color[i]
            self.nodes.append(node)

    def initialise_network_of_nodes(self):
        for i in range(self.num_nodes):
            node = self.nodes[i]
            neighbors = self.select_k_neighbors(node)
            node.neighbors = neighbors

    def communicate(self, node):
        random_neighbor = node.select_random_neighbor(self.k)

        current_node_identifiers = node.get_identifiers() + [node]
        random_neighbor_identifiers = random_neighbor.get_identifiers() + [random_neighbor]

        node.update_neighbors(random_neighbor_identifiers, self.k)
        random_neighbor.update_neighbors(current_node_identifiers, self.k)

    def evolve_network(self):
        for _ in range(self.epochs):
            for i in range(self.num_nodes):
                self.communicate(self.nodes[i])
        file_name = "/Users/anmol/Desktop/nodes_{}.txt".format(self.epochs)
        # self.write_network_topology_to_file(file_name)
        self.plot_red_nodes()

    def write_network_topology_to_file(self, file_name):
        with open(file_name, 'w+') as f:
            for i in range(self.num_nodes):
                neighbor_ids = [str(node.id) for node in self.nodes[i].neighbors]
                f.write(str(self.nodes[i].id) + "~" + self.nodes[i].color + " : " + ",".join(neighbor_ids) + "\n")

    def plot_red_nodes(self):
        red_nodes = filter(lambda x: x.color == 'red', self.nodes)
        red_node_neighbors = set([nei for red_node in red_nodes for nei in red_node.neighbors])
        rgb, X, Y = [], [], []
        for node in red_nodes:
            rgb.append(node.r_g_b)
            X.append(node.position.x)
            Y.append(node.position.y)

        for node in red_node_neighbors:
            rgb.append(node.r_g_b)
            X.append(node.position.x)
            Y.append(node.position.y)

        colors = np.array([[abs(i[0]), abs(i[1]), abs(i[2])] for i in rgb])
        # print(colors)
        plt.xlim(-math.pi, math.pi)
        plt.scatter(X, Y, c=colors / 255.0, s=30)
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    ring_topology = Topology("Ring", 20, 10, 5, None, None)
    m = 5
    r_m = [i*i + 1 for i in range(m)]
    dynamic_ring_topology = Topology("Dynamic_Ring", 20, 6, 5, m, r_m)
