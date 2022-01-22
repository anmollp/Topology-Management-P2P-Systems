import math
import matplotlib.pyplot as plt
import random
import networkx as nx

from node import Node
from utils import Utils


class Ring:
    def __init__(self, num_nodes, k, epochs):
        self.num_nodes = num_nodes
        self.epochs = epochs
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
        for i in range(self.num_nodes):
            node = self.nodes[i]
            neighbors = Utils.select_k_neighbors(node, self.nodes, self.k)
            node.neighbors = neighbors

    def communicate(self, node, one_way=False):
        random_neighbor = node.select_random_neighbor(self.k)

        current_node_identifiers = node.get_identifiers() + [node]
        if not one_way:
            random_neighbor_identifiers = random_neighbor.get_identifiers() + [random_neighbor]
            node.update_neighbors(random_neighbor_identifiers, self.k)

        random_neighbor.update_neighbors(current_node_identifiers, self.k)

    def evolve_network(self):
        network_color_file_name = "/Users/anmol/Desktop/node_colors.txt"
        self.write_network_color_to_file(network_color_file_name)
        for _ in range(self.epochs):
            for i in range(self.num_nodes):
                self.communicate(self.nodes[i])
        file_name = "/Users/anmol/Desktop/nodes_{}.txt".format(self.epochs)
        self.write_network_topology_to_file(file_name)

        self.plot_network("red", "/Users/anmol/Desktop/red_nodes_{}.jpg".format(self.epochs))
        self.plot_network("green", "/Users/anmol/Desktop/green_nodes_{}.jpg".format(self.epochs))
        self.plot_network("blue", "/Users/anmol/Desktop/blue_nodes_{}.jpg".format(self.epochs))

    def write_network_color_to_file(self, file_name):
        with open(file_name, 'w+') as f:
            for i in range(self.num_nodes):
                f.write(str(self.nodes[i].id) + " " + self.nodes[i].color + "\n")

    def write_network_topology_to_file(self, file_name):
        with open(file_name, 'w+') as f:
            for i in range(self.num_nodes):
                neighbor_ids = [str(node.id) for node in self.nodes[i].neighbors]
                f.write(str(self.nodes[i].id) + " : " + ",".join(neighbor_ids) + "\n")

    def plot_network(self, color, image_file_name):
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
        nx.draw_networkx(graph, pos, node_color=color_map, edge_color=color_map)
        plt.grid('on')
        plt.savefig(image_file_name)
        print(nx.is_connected(graph))
        graph.clear()
        plt.clf()


if __name__ == "__main__":
    ring_topology = Ring(10, 3, 40)
