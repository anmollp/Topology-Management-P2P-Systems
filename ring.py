import math
import matplotlib.pyplot as plt
import random
import networkx as nx

from node import Node
from utils import Utils


class Ring:
    def __init__(self, num_nodes, k, epochs):
        self.num_nodes = num_nodes
        self.epochs = epochs + 1
        self.nodes = []
        self.k = k
        self.counter = 0
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
        """
        get random colored nodes from red green and blue
        :param groups: number of color groups
        :param points_set: a set of points with a specified x,y position on the topology curve
        :return: colored nodes
        """
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

    def build_nodes(self):
        """
        build the topology with user input number of nodes on a ring
        :return:
        """
        theta = [2 * math.pi / self.num_nodes * i for i in range(self.num_nodes)]
        co_ordinates = set((math.cos(t), math.sin(t)) for t in theta)

        colored_nodes = self.get_nodes_color_randomized(3, co_ordinates)
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

    def initialise_network_of_nodes(self):
        """
        Initiate network building
        :return:
        """
        for i in range(self.num_nodes):
            node = self.nodes[i]
            neighbors = Utils.select_k_neighbors(node, self.nodes, self.k)
            node.neighbors = neighbors

    def communicate(self, node, one_way=False):
        """
        Communication between a node and its randomly selected neighbor
        :param node: the node that initiates communication
        :param one_way: if true initiate only a one-sided communication otherwise a two-way communication
        :return:
        """
        random_neighbor = node.select_random_neighbor(self.k)

        current_node_identifiers = node.get_identifiers() + [node]
        if not one_way:
            random_neighbor_identifiers = random_neighbor.get_identifiers() + [random_neighbor]
            node.update_neighbors(random_neighbor_identifiers, self.k)

        random_neighbor.update_neighbors(current_node_identifiers, self.k)

    def evolve_network(self):
        """
        Network evolution
        :return:
        """
        network_color_file_name = "/Users/anmol/Desktop/EEL6761/R_N{}_k{}.txt".format(self.num_nodes, self.k)
        Utils.write_network_color_to_file(self.nodes, network_color_file_name)
        for i in range(1, self.epochs):
            for j in range(self.num_nodes):
                self.communicate(self.nodes[j])
            if i % 5 == 0:
                colors = ["red", "green", "blue"]
                for color in colors:
                    image_file_name = "/Users/anmol/Desktop/EEL6761/R_N{}_k{}_{}_{}.jpg".format(self.num_nodes, self.k,
                                                                                                color, i)
                    self.plot_network(color, image_file_name)
                    file_name = "/Users/anmol/Desktop/EEL6761/R_N{}_k{}_{}_{}.txt".format(self.num_nodes, self.k, color,
                                                                                          i)
                    Utils.write_network_topology_to_file(self.nodes, file_name)

    def plot_network(self, color, image_file_name):
        """
        Visualising the network at current instant of time.
        :param color: color of interest in visualizing
        :param image_file_name: a file to capture the network snapshot
        :return:
        """
        nodes = set(filter(lambda x: x.color == color, self.nodes))
        node_neighbors = set([nei for node in nodes for nei in node.neighbors])

        all_nodes = nodes.union(node_neighbors)

        rgb, X, Y = [], [], []
        position = {}
        color_map = []

        for node in all_nodes:
            rgb.append(node.r_g_b)
            X.append(node.position.x)
            Y.append(node.position.y)
            position[node.id] = (node.position.x, node.position.y)
            color_map.append(Utils.convert_to_hex(tuple(node.r_g_b)))

        edges = [(node.id, nei.id) for node in nodes for nei in node.neighbors]

        graph = nx.Graph()
        for key, value in position.items():
            graph.add_node(key, pos=value)
        graph.add_edges_from(edges)

        pos = nx.get_node_attributes(graph, 'pos')
        nx.draw_networkx(graph, pos, node_color=color_map, node_size=5, with_labels=False, edge_color=color_map)
        plt.grid('on')
        plt.savefig(image_file_name)
        print(nx.is_connected(graph))
        graph.clear()
        plt.clf()


if __name__ == "__main__":
    ring_topology = Ring(45, 3, 40)
