
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from queue import PriorityQueue
from matplotlib.patches import Polygon

x_max = 600
y_max = 250

Hex = [[300, 50], [364, 87], [364, 162], [300, 200], [235, 162], [235, 87]]

Hex_Clear = [[300, 45], [370, 85], [370, 165], [300, 205], [230, 165], [230, 85]]

Rect1 = [[100, 150], [150, 150], [150, 250], [100, 250]]

Rect1_clear = [[95, 145], [155, 145], [155, 250], [95, 250]]

Rect2 = [[100, 0], [150, 0], [150, 100], [100, 100]]

Rect2_clear = [[95, 0], [155, 0], [155, 105], [95, 105]]

Tri = [[460, 25], [510, 125], [460, 225]]

Tri_clear = [[455, 5], [515, 125], [455, 245]]


def Equ_line(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - (slope * x1)
    return [slope, intercept]


def Rec_inside1(point):
    x, y = point
    bl = [95, 145]
    ur = [155, 250]
    if ((x >= bl[0] and x <= ur[0]) and (y >= bl[1] and y <= ur[1])):
        return True
    return False


def Rec_inside(point):
    x, y = point
    bl = [95, 0]
    ur = [155, 105]
    if ((x >= bl[0] and x <= ur[0]) and (y >= bl[1] and y <= ur[1])):
        return True
    return False


def Hex_inside(point):
    x, y = point
    equ1 = Equ_line(Hex[0], Hex[1])
    l1_flag = y - equ1[0] * x - equ1[1] >= 0
    l2_flag = x <= Hex[1][0]
    equ3 = Equ_line(Hex_Clear[2], Hex_Clear[3])
    l3_flag = y - equ3[0] * x - equ3[1] <= 0
    equ4 = Equ_line(Hex_Clear[3], Hex_Clear[4])
    l4_flag = y - equ4[0] * x - equ4[1] <= 0
    l5_flag = x >= Hex_Clear[4][0]
    equ6 = Equ_line(Hex_Clear[5], Hex_Clear[0])
    l6_flag = y - equ6[0] * x - equ6[1] >= 0

    flag = l1_flag and l2_flag and l3_flag and l4_flag and l5_flag and l6_flag
    return flag



def Tri_inside(point):
    x, y = point
    l1_flag = x >= 455
    equ2 = Equ_line(Tri_clear[2], Tri_clear[1])
    l2_flag = y - equ2[0] * x - equ2[1] <= 0
    equ3 = Equ_line(Tri_clear[1], Tri_clear[0])
    l3_flag = y - equ3[0] * x - equ3[1] >= 0
    flag = l1_flag and l2_flag and l3_flag
    return flag


def check_obstacle(current_node):
    x, y = current_node
    if (x > x_max) or (y > y_max) or (x < 0) or (y < 0):
    # if (x < 0) or (y < 0):
        return False
    if (Hex_inside(current_node) or Rec_inside1(current_node) or Rec_inside(current_node) or Tri_inside(current_node)):
        return False
    return True


def get_shapes():
    hex_clear = Polygon([Hex_Clear[0], Hex_Clear[1], Hex_Clear[2], Hex_Clear[3], Hex_Clear[4], Hex_Clear[5]],
                        facecolor='r')
    Hexagon = Polygon([Hex[0], Hex[1], Hex[2], Hex[3], Hex[4], Hex[5]], facecolor='b')
    rect_1_clear = Polygon([Rect1_clear[0], Rect1_clear[1], Rect1_clear[2], Rect1_clear[3]], facecolor='r')
    rect_1 = Polygon([Rect1[0], Rect1[1], Rect1[2], Rect1[3]], facecolor='b')
    rect_2_clear = Polygon([Rect2_clear[0], Rect2_clear[1], Rect2_clear[2], Rect2_clear[3]], facecolor='r')
    rect_2 = Polygon([Rect2[0], Rect2[1], Rect2[2], Rect2[3]], facecolor='b')
    tri_clear = Polygon([Tri_clear[0], Tri_clear[1], Tri_clear[2]], facecolor='r')
    tri = Polygon([Tri[0], Tri[1], Tri[2]], facecolor='b')
    return (hex_clear, Hexagon, rect_1_clear, rect_1, rect_2_clear, rect_2, tri_clear, tri)


def CheckNeighbour(current_node):
    neighbors = []
    x, y = current_node
    actions = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]
    for action in actions:
        if check_obstacle((x + action[0], y + action[1])):
            if action[0] != 0 and action[1] != 0:
                neighbors.append([(x + action[0], y + action[1]), 1.4])
            else:
                neighbors.append([(x + action[0], y + action[1]), 1])
    return neighbors


def dijkstra_algo(source, dst):
    Open = {}
    Close = {}

    Open[source] = 0
    Closeed = []

    queue = PriorityQueue()
    queue.put((Open[source], source))
    path = []
    while queue:
        current_node = queue.get()[1]
        print("Node : ", current_node)
        if current_node == dst:
            print("Found!!")
            temp = dst
            while (Close[temp] != source):
                path.append(Close[temp])
                temp = Close[temp]
            break
        if current_node not in Closeed:
            if (check_obstacle(current_node)):
                Closeed.append(current_node)
            neighbors = CheckNeighbour(current_node)
            for neighbor, cost in neighbors:
                node_cost = Open[current_node] + cost
                if (not Open.get(neighbor)):
                    Open[neighbor] = node_cost
                    Close[neighbor] = current_node
                else:
                    if (node_cost < Open[current_node]):
                        Open[neighbor] = node_cost
                        Close[neighbor] = current_node
                queue.put((Open[neighbor], neighbor))
    return path, Closeed


def init():
    scatter_plot.set_offsets([])
    return scatter_plot


def ani(index, last_Closeed):
    if (index <= last_Closeed):
        line.set_data(path_x[0], path_y[0])
        data = np.hstack((Closeed_x[:index, np.newaxis], Closeed_y[:index, np.newaxis]))
        scatter_plot.set_offsets(data)
    else:
        line.set_data(path_x[:(index - last_Closeed) * 30], path_y[:(index - last_Closeed) * 30])
    return scatter_plot, line


if __name__ == "__main__":
    source_x, source_y, dst_x, dst_y = 0, 0, 0, 0

    while True:
        print("Enter source points as X,Y :")
        source = input()
        source_x = int(source.split(",")[0])
        source_y = int(source.split(",")[1])

        print("Enter dst points as X,Y :")
        dst = input()
        dst_x = int(dst.split(",")[0])
        dst_y = int(dst.split(",")[1])

        if (check_obstacle([source_x, source_y]) and check_obstacle([dst_x, dst_y])):
            break
        else:
            print("Please enter valid Input")
            continue

    source = (source_x, source_y)
    dst = (dst_x, dst_y)
    print("Source is : ", source)
    print("dst is : ", dst)

    fig = plt.figure()
    axis = plt.axes(xlim=(0, 600), ylim=(0, 250))
    axis.set_facecolor('k')

    path, Closeed = dijkstra_algo(source, dst)
    path.append(source)
    path.insert(0, dst)

    Closeed_x, Closeed_y = (np.array(Closeed)[:, 0], np.array(Closeed)[:, 1])

    path_x, path_y = (np.array(path)[:, 0], np.array(path)[:, 1])

    line, = axis.plot(path_x, path_y, color='g')
    scatter_plot = axis.scatter([], [], s=2, color='w')

    shapes = get_shapes()
    for index in shapes:
        axis.add_patch(index)

    animator = FuncAnimation(fig, ani, frames=(len(Closeed) + len(path)), fargs=[len(Closeed)], interval=0.01,
                             repeat=False, blit=True)
    plt.show()
