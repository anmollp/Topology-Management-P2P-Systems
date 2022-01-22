import math
import random
import matplotlib.pyplot as plt
from collections import deque
import networkx as nx

from utils import Utils
from node import Node
from TwoDPoint import TwoDPoint


class DynamicRing:
    """
    Dynamic Ring Topology
    """
    def __init__(self, num_nodes, k, m, radii):
        self.num_nodes = num_nodes
        self.epochs = m * 5
        self.nodes = []
        self.new_nodes = []
        self.num_new_nodes = 0
        self.k = k
        self.iteration = 1
        self.radii = deque(radii)
        self.radius = 1
        self.build_nodes()
        self.initialise_network_of_nodes()
        self.evolve_network()

    @staticmethod
    def get_nodes_color_randomized(points_set: set, num_nodes):
        """
        get random colored nodes
        :param points_set: a set of points with a specified x,y position on the topology curve
        :param num_nodes: total number of nodes in the topology
        :return: colored nodes
        """
        points_colored = []

        for i in range(num_nodes):
            point = random.choice(tuple(points_set))
            r, g, b, color = Utils.get_random_color()
            points_colored.append((point, r, g, b, color))
            points_set.remove(point)

        return points_colored

    def build_nodes(self):
        """
        build the topology with user input number of nodes on a ring
        :return:
        """
        theta = [2 * math.pi / self.num_nodes * i for i in range(self.num_nodes)]
        co_ordinates = set((self.radius * math.cos(t), self.radius * math.sin(t)) for t in theta)

        colored_nodes = self.get_nodes_color_randomized(co_ordinates, self.num_nodes)
        points, red, green, blue, color = zip(*colored_nodes)

        X, Y, Z = Utils.transform_rgb_to_xyz(red, green, blue)
        l, a, b = Utils.transform_xyz_to_cie_l_ab(X, Y, Z)

        for i in range(0, self.num_nodes):
            node = Node(i, points[i][0], points[i][1])
            node.l_distance = l[i]
            node.a_distance = a[i]
            node.b_distance = b[i]
            node.r_g_b = [red[i], green[i], blue[i]]
            node.color = color[i]
            self.nodes.append(node)

    def add_build_nodes(self):
        """
        Dynamically change the ring to increase in radius and allow additional nodes to join the topology
        :return:
        """
        total_nodes = self.num_nodes + self.num_new_nodes
        theta = [2 * math.pi / total_nodes * i for i in range(total_nodes)]
        co_ordinates = set((self.radius * math.cos(t), self.radius * math.sin(t)) for t in theta)

        new_nodes = self.get_nodes_color_randomized(co_ordinates, self.num_new_nodes)
        points, red, green, blue, color = zip(*new_nodes)

        X, Y, Z = Utils.transform_rgb_to_xyz(red, green, blue)
        l, a, b = Utils.transform_xyz_to_cie_l_ab(X, Y, Z)

        start = self.num_nodes
        end = self.num_nodes + self.num_new_nodes
        for i in range(start, end):
            node = Node(i, points[i - start][0], points[i - start][1])
            node.l_distance = l[i - start]
            node.a_distance = a[i - start]
            node.b_distance = b[i - start]
            node.r_g_b = [red[i - start], green[i - start], blue[i - start]]
            node.color = color[i - start]
            self.new_nodes.append(node)

        for i in range(0, self.num_nodes):
            point = random.choice(tuple(co_ordinates))
            co_ordinates.remove(point)
            self.nodes[i].position = TwoDPoint(point[0], point[1])
            self.nodes[i].update_neighbors(self.new_nodes, self.k)

        for i in range(start, end):
            all_nodes = self.nodes + self.new_nodes
            self.new_nodes[i - start].update_neighbors(all_nodes, self.k)

        self.num_nodes = total_nodes

        self.nodes = self.nodes + self.new_nodes

    def initialise_network_of_nodes(self):
        """
        Initiate network building
        :return:
        """
        for i in range(self.num_nodes):
            node = self.nodes[i]
            neighbors = Utils.select_k_neighbors(node, self.nodes, self.k)
            node.neighbors = neighbors

    def communicate(self, node):
        """
        Communication between a node and its randomly selected neighbor
        :param node: the node that initiates communication
        :return:
        """
        random_neighbor = node.select_random_neighbor(self.k)

        current_node_identifiers = node.get_identifiers() + [node]
        random_neighbor_identifiers = random_neighbor.get_identifiers() + [random_neighbor]

        node.update_neighbors(random_neighbor_identifiers, self.k)
        random_neighbor.update_neighbors(current_node_identifiers, self.k)

    def evolve_network(self):
        """
        Network evolution and dynamic change in ring topology for every 5th epoch
        :return:
        """
        for _ in range(self.epochs):
            if self.iteration % 5 == 0:
                self.rearrange_nodes()
            for i in range(self.num_nodes):
                self.communicate(self.nodes[i])
            if self.iteration == 1 or self.iteration % 5 == 0:
                file_name = "/Users/anmol/Desktop/nodes_{}.txt".format(self.iteration)
                self.write_network_topology_to_file(file_name)
                image_file_name = "/Users/anmol/Desktop/all_nodes_{}.png".format(self.iteration)
                self.plot_network(image_file_name)
            self.iteration += 1

    def rearrange_nodes(self):
        """
        Change the radius of the topology and include new nodes.
        :return:
        """
        self.num_new_nodes = new_radius = self.radii.popleft()
        self.radius = new_radius
        self.add_build_nodes()
        self.new_nodes = []

    def write_network_topology_to_file(self, file_name):
        """A writer method that writes current topology to a file"""
        with open(file_name, 'w+') as f:
            for i in range(self.num_nodes):
                neighbor_ids = [str(node.id) for node in self.nodes[i].neighbors]
                f.write(str(self.nodes[i].id) + " " + self.nodes[i].color + " : " + ",".join(neighbor_ids) + "\n")

    def plot_network(self, image_file_name):
        """
        Visualising the network at current instant of time.
        :param image_file_name: a file to capture the network snapshot
        :return:
        """
        position = {}
        rgb, X, Y = [], [], []
        color_map = []

        for node in self.nodes:
            rgb.append(node.r_g_b)
            X.append(node.position.x)
            Y.append(node.position.y)
            position[node.id] = (node.position.x, node.position.y)
            color_map.append(Utils.convert_to_hex(tuple(node.r_g_b)))

        edges = [(node.id, nei.id) for node in self.nodes for nei in node.neighbors]

        graph = nx.Graph()
        for key, value in position.items():
            graph.add_node(key, pos=value)
        graph.add_edges_from(edges)

        pos = nx.get_node_attributes(graph, 'pos')
        nx.draw_networkx(graph, pos, node_color=color_map, node_size=5, with_labels=False, edge_color=color_map)
        plt.grid('on')
        plt.savefig(image_file_name)
        graph.clear()
        plt.clf()


if __name__ == "__main__":
    radii = [2, 3, 5, 7, 8]
    drt = DynamicRing(10, 3, 5, radii)
