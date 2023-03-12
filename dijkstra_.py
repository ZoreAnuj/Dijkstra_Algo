import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from queue import PriorityQueue
from matplotlib.patches import Polygon

x_max, Y = 600, 250
Hex1, Hex2, Hex3, Hex4, Hex5, Hex6 = [300, 50], [364, 87], [364, 162], [300, 200], [235, 162], [235, 87]
Hex1_clear, Hex2_clear,Hex3_clear, Hex4_clear,Hex5_clear,Hex6_clear = [300, 45], [370, 85], [370, 165], [300, 205], [230, 165], [230, 85]
Rect_1_1,Rect_1_2,Rect_1_3,Rect_1_4 = [100, 150], [150, 150], [150, 250], [100, 250]
Rect_1_1_clear, Rect_1_2_clear, Rect_1_3_clear, Rect_1_4_clear = [95,145], [155,145], [155, 250], [95, 250]
Rect_2_1,Rect_2_2,Rect_2_3,Rect_2_4 = [100, 0], [150, 0], [150, 100], [100, 100]
Rect_2_1_clear, Rect_2_2_clear, Rect_2_3_clear, Rect_2_4_clear = [95,0], [155,0], [155, 105], [95, 105]
Tri1, Tri2, Tri3 = [460,25], [510, 125], [460, 225]
Tri1_clear, Tri2_clear, Tri3_clear = [455, 5], [515, 125], [455, 245]

def init():
    SPlot.set_offsets([])
    return SPlot

def Obs(Node_C):
    def Line(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        delY = (y2 - y1)
        delX = (x2 - x1)
        m = delY/delX
        ipt = y1-(m*x1)
        arr = [m, ipt]
        return arr
    
    def Hex(point):
        x, y = point
        eq1 = Line(Hex1_clear, Hex2_clear)
        eq2 = lambda x: x <= Hex2_clear[0]
        eq3 = Line(Hex3_clear, Hex4_clear)
        eq4 = Line(Hex4_clear, Hex5_clear)
        eq5 = lambda x: x >= Hex5_clear[0]
        eq6 = Line(Hex6_clear, Hex1_clear)
        l1_flag = y - eq1[0]*x - eq1[1] >= 0
        l2_flag = eq2(x)
        l3_flag = y - eq3[0]*x - eq3[1] <= 0
        l4_flag = y - eq4[0]*x - eq4[1] <= 0
        l5_flag = eq5(x)
        l6_flag = y - eq6[0]*x - eq6[1] >= 0
        flag = l1_flag and l2_flag and l3_flag and l4_flag and l5_flag and l6_flag
        return flag
    def Rect1(point):
        x, y = point
        bl = [95,145]
        ur = [155,250]
        if((x>=bl[0] and x<=ur[0]) and (y>=bl[1] and y<=ur[1])):
            return True
        return False

    def Rect(point):
        x, y = point
        bl = [95,0]
        ur = [155,105]
        if((x>=bl[0] and x<=ur[0]) and (y>=bl[1] and y<=ur[1])):
            return True
        else:
            return False
    
    def Tri(point):
        x, y = point
        l1_flag = x >= 455
        eq2 = Line(Tri3_clear, Tri2_clear)
        l2_value = y - eq2[0]*x - eq2[1]
        l2_flag = l2_value <= 0
        eq3 = Line(Tri2_clear, Tri1_clear)
        l3_value = y - eq3[0]*x - eq3[1]
        l3_flag = l3_value >= 0
        flag = l1_flag and l2_flag and l3_flag
        return flag

    x, y = Node_C
    if x < 0 or y < 0 or x > x_max or y > Y:
        return False
    if Hex(Node_C) or Rect1(Node_C) or Rect(Node_C) or Tri(Node_C):
        return False
    return True

def Object_Clearance():
    Tri_clear = Polygon([Tri1_clear, Tri2_clear, Tri3_clear], facecolor = 'g')
    Tri = Polygon([Tri1, Tri2, Tri3], facecolor = 'r')
    Hex_clear = Polygon([Hex1_clear, Hex2_clear, Hex3_clear, Hex4_clear, Hex5_clear, Hex6_clear], facecolor = 'g')
    Hex = Polygon([Hex1, Hex2, Hex3, Hex4, Hex5, Hex6], facecolor = 'r')
    Rect_1 = Polygon([Rect_1_1, Rect_1_2, Rect_1_3, Rect_1_4], facecolor = 'r')
    Rect_1_clear = Polygon([Rect_1_1_clear, Rect_1_2_clear, Rect_1_3_clear, Rect_1_4_clear], facecolor = 'g')
    Rect_2_clear = Polygon([Rect_2_1_clear, Rect_2_2_clear, Rect_2_3_clear, Rect_2_4_clear], facecolor = 'g')
    Rect_2 = Polygon([Rect_2_1, Rect_2_2, Rect_2_3, Rect_2_4], facecolor = 'r')
    return (Hex_clear, Hex, Rect_1_clear, Rect_1, Rect_2_clear, Rect_2, Tri_clear, Tri)

def dijkstra(src, dst):
    def FindNeighbour(Node_C):
        Neigs = []
        x, y = Node_C
        actions = [[1,0], [-1,0], [0,1], [0,-1], [1,1], [-1,1], [1,-1], [-1,-1]]
        for action in actions:
            next_node = (x + action[0], y + action[1])
            if Obs(next_node):
                cost = 1.4 if action[0] != 0 and action[1] != 0 else 1
                Neigs.append([next_node, cost])
        return Neigs
    
    OList, CList={}, {}
    OList[src] = 0
    V, P = [],[]
    queue = PriorityQueue()
    queue.put((OList[src], src))
    while queue:
        Node_C = queue.get()[1]
        print("Current node : ", Node_C)
        if Node_C == dst:
            print("Found!!")
            temp = dst
            while(CList[temp]!=src):
                P.append(CList[temp])
                temp = CList[temp]
            break
        if Node_C not in V:
            if(Obs(Node_C)):
                V.append(Node_C)
            Neigs = FindNeighbour(Node_C)
            for Neig, cost in Neigs:
                node_cost = OList[Node_C] + cost
                if (not OList.get(Neig)):
                    OList[Neig], CList[Neig] = node_cost, Node_C
                else:
                    if(node_cost<OList[Node_C]):
                        OList[Neig], CList[Neig] = node_cost, Node_C
                queue.put((OList[Neig], Neig))
    return P, V

def Anime(idx, last_V):
    if(idx<=last_V):
        line.set_data(XP[0], YP[0])
        d = np.hstack((V_x[:idx,np.newaxis], V_y[:idx, np.newaxis]))
        SPlot.set_offsets(d)
    else:
        line.set_data(XP[:(idx-last_V)*30], YP[:(idx-last_V)*30])
    return SPlot, line

if __name__ == "__main__":
    src_x, src_y, dst_x, dst_y = 0, 0, 0, 0

    while True:
        print("Enter source points (X,Y) :")
        src = input()
        src_x, src_y = int(src.split(",")[0]), int(src.split(",")[1])
            
        print("Enter destination points (X,Y) :")
        dst = input()
        dst_x, dst_y = int(dst.split(",")[0]), int(dst.split(",")[1])
    
        if(Obs([src_x, src_y]) and Obs([dst_x, dst_y])):
            break
        else:
            print("Invalid Input! Retry")
            continue

    src, dst = (src_x, src_y), (dst_x, dst_y)
    print("Source is : ", src)
    print("Destination is : ", dst)

    fig = plt.figure()
    axis = plt.axes(xlim=(0, 600), ylim=(0, 250))
    axis.set_facecolor('k')

    P, V = dijkstra(src, dst)
    P.append(src)
    P.insert(0, dst)

    V_x, V_y = (np.array(V)[:,0], np.array(V)[:,1])
    XP, YP = (np.array(P)[:,0], np.array(P)[:,1])

    line, = axis.plot(XP, YP, color = 'g')
    SPlot = axis.scatter([], [], s=2, color='w')

    S = Object_Clearance()
    for idx in S:
        axis.add_patch(idx)

    animator = FuncAnimation(fig, Anime, frames = (len(V)+len(P)) ,fargs=[len(V)], interval=0.01, repeat=False, blit=True)
    plt.show()
