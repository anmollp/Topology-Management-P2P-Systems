import random
import numpy as np
import math
import os


class Utils:
    """A utility class for methods frequently used in building a topology"""

    def __init__(self):
        pass

    @staticmethod
    def get_homework_directory():
        home = os.path.expanduser("~")
        homework_directory = os.path.join(home, "Patil_EEL6761_HW1")
        return homework_directory

    @staticmethod
    def get_random_color():
        """
        :return: a tuple of redness, greenness, blueness
        """
        r, g, b, color = random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255), ""
        return r, g, b, color

    @staticmethod
    def get_red_color():
        """
        :return: a tuple of redness, greenness, blueness
        """
        r, g, b, color = random.randrange(200, 255), random.randrange(0, 80), random.randrange(0, 80), "red"
        return r, g, b, color

    @staticmethod
    def get_green_color():
        """
        :return: a tuple of redness, greenness, blueness
        """
        r, g, b, color = random.randrange(0, 80), random.randrange(200, 255), random.randrange(0, 80), "green"
        return r, g, b, color

    @staticmethod
    def get_blue_color():
        """
        :return: a tuple of redness, greenness, blueness
        """
        r, g, b, color = random.randrange(0, 80), random.randrange(0, 80), random.randrange(200, 255), "blue"
        return r, g, b, color

    @staticmethod
    def transform_rgb_to_xyz(r, g, b):
        """
        Convert R G B values to X Y Z based on the formula provided
        :param r: Red vector containing redness values on a scale of 0 to 255
        :param g: Green vector containing greenness values on a scale of 0 to 255
        :param b: Blue vector containing blueness values on a scale of 0 to 255
        :return: X Y Z values
        """
        sR = np.array(r)
        sG = np.array(g)
        sB = np.array(b)

        var_R = (sR / 255.0)
        var_G = (sG / 255.0)
        var_B = (sB / 255.0)

        var_R = [((vR + 0.055) / 1.055) ** 2.4 if vR > 0.04045 else vR / 12.92 for vR in var_R]
        var_G = [((vG + 0.055) / 1.055) ** 2.4 if vG > 0.04045 else vG / 12.92 for vG in var_G]
        var_B = [((vB + 0.055) / 1.055) ** 2.4 if vB > 0.04045 else vB / 12.92 for vB in var_B]

        var_R = [vR * 100 for vR in var_R]
        var_G = [vG * 100 for vG in var_G]
        var_B = [vB * 100 for vB in var_B]

        X = np.array(var_R) * 0.4124 + np.array(var_G) * 0.3576 + np.array(var_B) * 0.1805
        Y = np.array(var_R) * 0.2126 + np.array(var_G) * 0.7152 + np.array(var_B) * 0.0722
        Z = np.array(var_R) * 0.0193 + np.array(var_G) * 0.1192 + np.array(var_B) * 0.9505

        return X, Y, Z

    @staticmethod
    def transform_xyz_to_cie_l_ab(x, y, z):
        """
        Convert X Y Z values to cie-l, cie-a, cie-b based on the formula provided
        :param x: X vector
        :param y: Y vector
        :param z: Z vector
        :return: cie-l, cie-a, cie-b
        """
        reference_x = 94.811
        reference_y = 100.00
        reference_z = 107.304

        var_X = x / reference_x
        var_Y = y / reference_y
        var_Z = z / reference_z

        var_X = np.array([vx ** (1 / 3) if vx > 0.008856 else (7.87 * vx) + (16 / 116) for vx in var_X])
        var_Y = np.array([vy ** (1 / 3) if vy > 0.008856 else (7.87 * vy) + (16 / 116) for vy in var_Y])
        var_Z = np.array([vz ** (1 / 3) if vz > 0.008856 else (7.87 * vz) + (16 / 116) for vz in var_Z])

        cie_l = (116 * var_Y) - 16
        cie_a = 500 * (var_X - var_Y)
        cie_b = 200 * (var_Y - var_Z)

        return cie_l, cie_a, cie_b

    @staticmethod
    def compute_distance(point_a, point_b):
        """
        Calculate the cie distance between two points
        :param point_a: 1st point
        :param point_b: 2nd point
        :return: distance between points
        """
        l = (point_b[0] - point_a[0]) ** 2
        a = (point_b[1] - point_a[1]) ** 2
        b = (point_b[2] - point_a[2]) ** 2
        delta = math.sqrt(l + a + b)
        return delta

    @staticmethod
    def convert_to_hex(rgba_color):
        """
        convert rgb to hex color
        :param rgba_color:
        :return: hex coding of color
        """
        red, green, blue = rgba_color
        return '#%02x%02x%02x' % (red, green, blue)

    @staticmethod
    def select_k_neighbors(node, all_nodes, k):
        """
        min heap based finding k nearest neighbors based on the distance criteria as provided in the assignment
        :param node: the node whose nearest neighbors is to be calculated
        :param all_nodes: set of all nodes
        :param k: the number of neighbors to choose
        :return: k nearest neighboring nodes
        """
        nodes = set(all_nodes)
        nodes.remove(node)
        k_nearest_neighbors = []

        n = k
        while n:
            neighbor = random.choice(tuple(nodes))
            k_nearest_neighbors.append(neighbor)
            nodes.remove(neighbor)
            n -= 1

        return k_nearest_neighbors

    @staticmethod
    def write_network_color_to_file(nodes, file_name):
        """
        A writer method that writes current topology nodes color to a file
        :param nodes: list of nodes
        :param file_name: a file to capture the colored network snapshot
        :return:
        """
        with open(file_name, 'w+') as f:
            for i in range(len(nodes)):
                f.write(str(nodes[i].id) + " " + nodes[i].color + "\n")

    @staticmethod
    def write_network_topology_to_file(nodes, file_name):
        """A writer method that writes current topology to a file"""
        with open(file_name, 'w+') as f:
            for i in range(len(nodes)):
                neighbor_ids = [str(node.id) for node in nodes[i].neighbors]
                f.write(str(nodes[i].id) + " : " + ",".join(neighbor_ids) + "\n")
