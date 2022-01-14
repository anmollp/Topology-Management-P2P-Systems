import random
import numpy as np
import math


class Utils:

    def __init__(self):
        pass

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
    def compute_distance(point_A, point_B):
        l = (point_B[0] - point_A[0]) ** 2
        a = (point_B[1] - point_A[1]) ** 2
        b = (point_B[2] - point_A[2]) ** 2
        delta = math.sqrt(l + a + b)
        return delta
