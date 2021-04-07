from helper_functions import *

def record_point(event, x, y, flag, param):
    global start_node, end_node
    Nodes, mat = param[0].copy(), param[1]

    if event == cv2.EVENT_LBUTTONDOWN:
        start_node = transform_and_make_node(mat, (x, y), start_node, Nodes, X, Y, img_adap)

    elif event == cv2.EVENT_RBUTTONDOWN:
        end_node = transform_and_make_node(mat, (x, y), end_node, Nodes, X, Y, img_adap)

    elif (event == cv2.EVENT_RBUTTONUP or event == cv2.EVENT_LBUTTONUP) and start_node != None and end_node != None:
        start_node.validate_and_connect(end_node, img_adap)
        solution_img, spots = find_shortest_path_for([start_node] + Nodes + [end_node])
        i_matrix = cv2.getPerspectiveTransform(pts2, pts1)
        solution_img = cv2.warpPerspective(solution_img, i_matrix, (500, 500))
        spots = cv2.warpPerspective(spots, i_matrix, (500, 500))
        solution_img = cv2.resize(solution_img, (X, Y))
        spots = cv2.resize(spots, (X, Y))
        cv2.imshow("solution_img", solution_img)
        solution_arena = ARENA.copy()
        solution_arena[solution_img > 100] = (0, 255, 0)
        solution_arena[spots > 100] = (0, 255, 255)
        cv2.imshow("ARENA", solution_arena)

if __name__ == "__main__":
    images = ['Arena.jpg', 'Arena1.jpg', 'Arena2.jpg', 'Arena3.png']

    filters = get_filters()

    for image in images:
        start_node = None
        end_node = None

        Arena = cv2.imread(image)
        arena = cv2.imread(image, 0)
        Y, X = 3*np.array(arena.shape)
        ARENA = cv2.resize(Arena, (X, Y))

        cv2.imshow("ARENA", ARENA)
        cv2.imshow("solution_img", np.zeros_like(ARENA))

        d = (500, 500)
        arena = cv2.resize(arena, d)
        Arena = cv2.resize(Arena, d)
        ######################################################### Image is resized

        _, th = cv2.threshold(arena, 128, 255, cv2.THRESH_BINARY)
        th_adap = cv2.adaptiveThreshold(arena, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 101, 2)
        ######################################################### Image is filtered

        Canny = cv2.Canny(th, 100, 200)
        contours, h = cv2.findContours(Canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        area = 0.0
        for c in contours:
            temp = cv2.contourArea(c)
            if temp > area:
                area = temp
                main_contour = c

        eps = 0.1 * cv2.arcLength(main_contour, True)
        poly_corners = np.squeeze(cv2.approxPolyDP(main_contour, eps, True))
        ######################################################### Arena corners are obtained

        poly_list = reorder(poly_corners)
        pts1 = np.float32(poly_list)
        pts2 = np.float32([(0, 0), (500, 0), (0, 500), (500, 500)])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        img1 = cv2.warpPerspective(arena, matrix, (500, 500))
        ######################################################### Arena from original gray image is transformed to 500*500 square

        img_adap = cv2.adaptiveThreshold(img1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 201, 2)
        img_adap = cv2.morphologyEx(img_adap, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8), iterations=1)
        _, img_adap = cv2.threshold(img_adap, 127, 255, cv2.THRESH_BINARY_INV)

        paths = apply_filters(img_adap.copy(), filters)
        nodes = np.zeros_like(paths[0])
        for i in range(len(paths)):
            _, paths[i] = cv2.threshold(paths[i], 127, 255//4, cv2.THRESH_BINARY)
            nodes += paths[i]

        _, nodes = cv2.threshold(nodes, 256//2 - 10, 255, cv2.THRESH_BINARY)
        ######################################################### Junctions are obtained in image (nodes)

        blank_image = np.zeros_like(nodes)

        contours, h = cv2.findContours(nodes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        img_adap_copy = img_adap.copy()
        nodes_list = []

        for c in contours:
            area = cv2.contourArea(c)
            if area > 900 or area < 40:
                cv2.fillPoly(nodes, [c], 0)
                cv2.fillPoly(img_adap, [c], 150)
            else:
                m = cv2.moments(c)
                x, y = int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"])
                nodes_list.append((x, y))
        ######################################################### True junction coordinates are stored in nodes_list

        Nodes = list(map(node, nodes_list))

        for i in range(len(Nodes)-1):
            for j in range(i+1, len(Nodes)):
                Nodes[i].validate_and_connect(Nodes[j], img_adap)
        ######################################################### Graph of nodes is formed

        cv2.setMouseCallback("ARENA", record_point, (Nodes, matrix))
        if cv2.waitKey(0) == ord("q"):
            break

    cv2.destroyAllWindows()