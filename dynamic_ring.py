import math
import random
import heapq
import matplotlib.pyplot as plt
from collections import deque
import networkx as nx

from utils import Utils
from node import Node
from TwoDPoint import TwoDPoint


class DynamicRing:
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
        points_colored = []

        for i in range(num_nodes):
            point = random.choice(tuple(points_set))
            r, g, b, color = Utils.get_random_color()
            points_colored.append((point, r, g, b, color))
            points_set.remove(point)

        return points_colored

    def build_nodes(self):
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
            if self.iteration % 5 == 0:
                self.rearrange_nodes()
            for i in range(self.num_nodes):
                self.communicate(self.nodes[i])
            if self.iteration == 1 or self.iteration % 5 == 0:
                file_name = "/Users/anmol/Desktop/nodes_{}.txt".format(self.iteration)
                self.write_network_topology_to_file(file_name)
                image_file_name = "/Users/anmol/Desktop/all_nodes_{}.jpg".format(self.iteration)
                self.plot_network(image_file_name)
            self.iteration += 1

    def rearrange_nodes(self):
        self.num_new_nodes = new_radius = self.radii.popleft()
        self.radius = new_radius
        self.add_build_nodes()
        self.new_nodes = []

    def write_network_topology_to_file(self, file_name):
        with open(file_name, 'w+') as f:
            for i in range(self.num_nodes):
                neighbor_ids = [str(node.id) for node in self.nodes[i].neighbors]
                f.write(str(self.nodes[i].id) + " " + self.nodes[i].color + " : " + ",".join(neighbor_ids) + "\n")

    def plot_network(self, image_file_name):
        position = {}
        rgb, X, Y = [], [], []
        color_map = []

        for node in self.nodes:
            rgb.append(node.r_g_b)
            X.append(node.position.x)
            Y.append(node.position.y)
            position[node.id] = (node.position.x, node.position.y)
            color_map.append(Utils.convert_to_hex(tuple(node.r_g_b)))
        # rgb, X, Y = [], [], []
        # for node in self.nodes:
        #     rgb.append(node.r_g_b)
        #     X.append(node.position.x)
        #     Y.append(node.position.y)

        # colors = np.array([[i[0], i[1], i[2]] for i in rgb])
        # plt.xlim(-math.pi, math.pi)
        # plt.scatter(X, Y, c=colors / 255.0, s=self.num_nodes)
        # plt.plot(X, Y)
        # # plt.grid(True)
        # plt.savefig(image_file_name)
        # plt.clf()
        edges = [(node.id, nei.id) for node in self.nodes for nei in node.neighbors]

        graph = nx.Graph()
        for key, value in position.items():
            graph.add_node(key, pos=value)
        graph.add_edges_from(edges)

        pos = nx.get_node_attributes(graph, 'pos')
        nx.draw_networkx(graph, pos, node_color=color_map)
        plt.grid('on')
        plt.savefig(image_file_name)
        graph.clear()
        plt.clf()


if __name__ == "__main__":
    radii = [2, 3, 5, 7, 8]
    drt = DynamicRing(45, 4, 5, radii)
