import numpy as np
import cv2
from helper_class import node

def transform_and_make_node(m, pt, initial_node, Nodes, X, Y, img_adap):
    x, y = pt[0]*500/X, pt[1]*500/Y
    pt = np.array([(x), (y), (1)])
    x, y, scale = np.dot(m, pt)
    x, y = np.int16(np.round((x/scale, y/scale), 0))

    temp = node((x, y))
    for Node in Nodes:
        temp.validate_and_connect(Node, img_adap)
    if list(temp.connections) == []:
        return initial_node
    else:
        return temp

def find_shortest_path_for(Nodes):
    ################## This function takes a list of node class objects and treats first and last element as start and end node respectively to find a shortest route
    for node in  Nodes:
        node.cost = np.inf
        node.nearest_node = None
    Nodes[-1].set_costs_in_chain()

    shortest_path_img = np.zeros((500, 500))
    node = Nodes[0]
    while node.cost != 0:
        shortest_path_img = cv2.line(shortest_path_img, tuple(node.coordinates), tuple(node.nearest_node.coordinates), 255, 7)
        node = node.nearest_node

    spots = np.zeros_like(shortest_path_img)
    cv2.rectangle(spots, tuple(Nodes[0].coordinates - 15), tuple(Nodes[0].coordinates + 15), 255, 3)
    cv2.circle(spots, tuple(Nodes[-1].coordinates), 15, 255, 5)

    return shortest_path_img, spots

def show_node_connections_of(nodes, name):
    ################## This function is used for debugging the code
    img = np.zeros((500, 500))
    for i, node in enumerate(nodes):
        for x, y in node.connections.keys():
            cv2.line(img, tuple(node.coordinates), (x, y), 255, 2)
    cv2.imshow(name, img)

def apply_filters(image, filters):
    new_images = []
    for filter in filters:
        new_images.append(cv2.filter2D(image, -1, filter))
    return new_images

def reorder(poly):
    ################## This function reorders the co-ordinates in the list poly, in clockwise direction starting from top left co-ordinate
    poly_list = [list(i) for i in poly]

    for i in range(1, 4):
        if poly_list[i][1] < poly_list[0][1] or poly_list[i][1] < poly_list[1][1]:
            poly_list.insert(0, poly_list.pop(i))

    for i in range(0, 4, 2):
        if poly_list[i][0] > poly_list[i + 1][0]:
            poly_list.insert(i, poly_list.pop(i + 1))

    return poly_list

def get_filters():
    filter_size = 81
    filter = np.zeros((filter_size, filter_size), dtype = np.float32)
    sfilter = filter.copy()

    filter[filter_size//2, :] = 1
    sfilter[range(filter_size), range(filter_size)] = 1

    filter = filter / (np.sum(filter))
    sfilter = sfilter / np.sum(sfilter)
    filters = []
    for i in range(2):
        filters.append(np.rot90(filter, i))

    for i in range(2):
        filters.append(np.rot90(sfilter, i))

    return filters
