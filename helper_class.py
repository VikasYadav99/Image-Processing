import numpy as np
import cv2

class node:
    def __init__(self, coordinates):
        self.coordinates = np.array(coordinates)
        self.connections = dict()
        self.cost = np.inf
        node.nearest_node = None

    def __sub__(self, node):
        square = (self.coordinates - node.coordinates)**2
        a, b = self.coordinates
        c, d = node.coordinates
        return ((c - a) ** 2 + (d - b) ** 2) ** 0.5

    def connect(self, node):
        distance = np.sum((self.coordinates - node.coordinates)**2) ** 0.5
        self.connections[tuple(node.coordinates)] = (node, distance)
        node.connections[tuple(self.coordinates)] = (self, distance)

    def validate_and_connect(a, b, img):
        thickness = 2
        blank_image = np.zeros_like(img)

        blank_image = cv2.line(blank_image, tuple(np.int16(np.round(a.coordinates, 0))), tuple(np.int16(np.round(b.coordinates, 0))), 255, thickness)
        image = cv2.bitwise_and(blank_image, img)

        distance = a - b
        pixels = np.sum(image) / (thickness * 255)

        if pixels / distance > 1.4: #1.4
            a.connect(b)

    def set_costs_in_chain(node):
        node_list = [node]
        node_list[-1].cost = 0

        while node_list != []:
            node = node_list.pop()
            for key in node.connections.keys():
                g = node.cost + node.connections[key][1]
                if node.connections[key][0].cost > g:
                    node_list.insert(0, node.connections[key][0])
                    node.connections[key][0].cost = g
                    node.connections[key][0].nearest_node = node