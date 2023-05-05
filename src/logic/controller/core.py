import numpy as np
import random
import pygame
import math
from math import atan2, degrees
from src.logic.controller.render import render_nodes
from src.simulator import GlobalConfig,Hook




# Debug options (show ids, get readings etc.)
def events_fn(*, objects, events, state):
    ret = dict()
    for event in events:
        if event.type == pygame.QUIT:
            ret["quit"] = True
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            if key == "i":
                if "display_ids" not in state: state["display_ids"] = True
                else: state["display_ids"] = not state["display_ids"]
            if key == "d":
                fname = input("Enter dump filename (dump.pkl): ")
                if fname == "": fname = "dump.pkl"
                objects.to_pickle(fname)
                print(f"Saved {fname}")
            if key == "a":
                if "display_active" not in state: state["display_active"] = False
                else: state["display_active"] = not state["display_active"]
                

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            nearest = objects.iloc[0]
            mindist = math.sqrt((nearest.x - pos[0])**2 + (nearest.y - pos[1])**2)
            for idx, object in objects.iterrows():
                dist = math.sqrt((object.x - pos[0])**2 + (object.y - pos[1])**2)
                if dist < mindist:
                    nearest = object
                    mindist = dist
            
            print(nearest)
    
    return ret


# Rendering functions
def render_fn(*, window, objects, state):
    nodes = objects[objects["type"] == "node"]
    render_nodes(nodes=nodes, window=window, state=state)


# -------------------------------------------------------------------------
def find_adjacent_nodes(nodes): # Return couple of nodes close adjacent
    cfg = GlobalConfig.cfg()
    adjacent_list_x = [nodes.x]
    adjacent_list_y = [nodes.y]
    id = [nodes.id]
    # print(adjacent_list_x,adjacent_list_y)
    vector = []
    result = []

    for i in list(zip(adjacent_list_x,adjacent_list_y,id)):
           vector = list(zip(i[0],i[1],i[2]))

    for j in vector:
        for s in vector:
            # print(j,s)
            distance = ((s[0] - j[0])**2 + (s[1] - j[1])**2)**0.5
            # print(distance)
            if distance <= (cfg.params.rs[0]*2): # (sensing radius * 2)
                result.append((j[2],s[2]))
                
    #print(result)
    return result


def find_neighbours(nodes,adjacent_nodes):
    for f in zip(nodes.id,nodes.x,nodes.y,nodes.fault):
        for i in adjacent_nodes:
            if f[0] == i[0]:
                for m in zip(nodes.id,nodes.x,nodes.y):
                    if i[1] == m[0]:
                        nodes.neighbours[f[0]].append([i[1],m[1],m[2]])
        if f[3] == False:
            nodes.neighbours[f[0]].remove([f[0],f[1],f[2]])
    #print(nodes.neighbours)
    return nodes.neighbours


def sort_coordinates(nodes):
    cx = 0
    cy = 0
    coords = []
    final_coords = []
    
    # print(nodes)
    for i in zip(nodes.neighbours,nodes.ordered_neighbours, nodes.id, nodes.x, nodes.y,nodes.fault):
        if i[5] == False:
            for k in i[0]:
                coords.append([k[1],k[2]])
            coords = np.array(coords)
            cx, cy = coords.mean(0)
            x, y = coords.T
            angles = np.arctan2(x-cx, y-cy)
            indices = np.argsort(angles)
            coords = coords[indices]
            final_coords = coords.tolist()
            i[1].append(final_coords)
            coords = []

    #print(nodes.ordered_neighbours)

    return nodes.ordered_neighbours


def add_id_to_neighours(nodes):
    for i in nodes.ordered_neighbours:
        for k in i:
            for r in k:
                for u in zip(nodes.id,nodes.x,nodes.y):
                    if r[0] == u[1] and r[1] == u[2]:
                        r.append(u[0])

def add_first_neighbour_to_the_end(neighbours):
    # i did this because the last node and the first one are adjacent
    first_neighbour = []
    for i in neighbours:
        if i:
            for u in i:
                first_neighbour = u[0]
                u.append(first_neighbour)
    return

def euclidean_distance(node1, node2):
    return math.sqrt((node2[0] - node1[0])**2 + (node2[1] - node1[1])**2)


def gabriel_graph(nodes):
#va benissimo solo che devo eliminare tutti i doppioni che sono tantissimi

    node1 = []
    node2 = []
    c = 0
    for i,l in zip(nodes.ordered_neighbours,nodes.gg_neighbours):
        if i:
            while c<len(i[0])-1:
                node1 = i[0][c]
                node2 = i[0][c+1]
                for j in zip(nodes.x,nodes.y,nodes.id):
                    if j[2] == node1[2] or j[2] == node2[2]:
                        continue
                    else:
                        distance1 = euclidean_distance(j, node1)
                        distance2 = euclidean_distance(j, node2)
                        distance12 = euclidean_distance(node1, node2)
                        if distance1 < distance12 and distance2 < distance12:
                            continue
                        else:
                            if node1 not in l :
                                l.append(node1)
                                l.append(node2)
                c+=1
            c=0
    #print((nodes.gg_neighbours)[0])
    return nodes.gg_neighbours

def add_first_neighbour_to_the_end_gg(gg_neighbour):
    first_neighbour = []
    for i in gg_neighbour:
        if i:
            first_neighbour = i[0]
            i.append(first_neighbour)
    return


def nodes_coordinates_id(nodes):
    nodes_coordinates = []
    for i in zip(nodes.id,nodes.x,nodes.y):
            nodes_coordinates.append(i)
    #print(nodes_coordinates)
    return nodes_coordinates

#---------------------------------------------------- untill here i need all the nodes

def circumcenter(a,b,c):
    d = 2 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
    ux = ((a[0] * a[0] + a[1] * a[1]) * (b[1] - c[1]) + (b[0] * b[0] + b[1] * b[1]) * (c[1] - a[1]) + (c[0] * c[0] + c[1] * c[1]) * (a[1] - b[1])) / d
    uy = ((a[0] * a[0] + a[1] * a[1]) * (c[0] - b[0]) + (b[0] * b[0] + b[1] * b[1]) * (a[0] - c[0]) + (c[0] * c[0] + c[1] * c[1]) * (b[0] - a[0])) / d
    return (ux, uy)


def find_circocentri(neighbours,node_coordinates):
    circocentri_middle = []
    circocentri = []
    s = 0
    for i,l in zip(neighbours,node_coordinates):
        if i:
            #print(i)
        # in i i have all the neigbhours of the node while in l i have node id and x and y
            c = [l[1],l[2],l[0]]
        # c is the node we are analyzing with (x,y,id)
            if len(i[0])>1:      
                while s < (len(i[0])-1):
                #devo saltare quelli con il neighbour vuoto senno non mi calcola nulla
                    a = [i[0][s][0],i[0][s][1]]
                    b = [i[0][s+1][0],i[0][s+1][1]]
                    f = [c[0],c[1]]
                    circ = circumcenter(a,b,f)
                    circocentri_middle.append([circ,c[2],c[0],c[1],i[0][s][2],i[0][s][0],i[0][s][1],i[0][s+1][2],i[0][s+1][0],i[0][s+1][1]])
                    #print('circocentri_middle',circocentri_middle)
                    #print('This is the circumcenter of :',i[0][s][2],',',i[0][s+1][2],',',c[2],'and is :',circ)
                    # circocentri è [[(x,y del circocentro),nodo importante, nodo2, nodo1]]
                    s+=1
                circocentri.append(circocentri_middle)
                circocentri_middle = []
                s = 0
    #print(circocentri)
    return circocentri

def find_circocentri_gg(gg_neighbours,node_coordinates):
    circocentri_middle = []
    circocentri = []
    s = 0
    for i,l in zip(gg_neighbours,node_coordinates):
        #print(i)
        if i:
            #print(i)
        # in i i have all the neigbhours of the node while in l i have node id and x and y
            c = [l[1],l[2],l[0]]
            #print('This is c',c)
        # c is the node we are analyzing with (x,y,id)      
            while s <(len(i)-1):
            #devo saltare quelli con il neighbour vuoto senno non mi calcola nulla
                a = [i[s][0],i[s][1]]
                b = [i[s+1][0],i[s+1][1]]
                f = [c[0],c[1]]
                circ = circumcenter(a,b,f)
                circocentri_middle.append([circ,c[2],c[0],c[1],i[s][2],i[s][0],i[s][1],i[s+1][2],i[s+1][0],i[s+1][1]])
                #print('This is the circumcenter of :',i[0][s][2],',',i[0][s+1][2],',',c[2],'and is :',circ)
                # circocentri è [[(x,y del circocentro),nodo importante, nodo2, nodo1]]
                s+=1
            circocentri.append(circocentri_middle)
            circocentri_middle = []
            s = 0
    #print(circocentri)
    return circocentri


def tent_rule(circocentri,nodes_coordinates,nodes_stuck,nodes_state):
    cfg = GlobalConfig.cfg()
    rs = cfg.params.rs[0]
    #(x - center_x)² + (y - center_y)² < radius²
    # print('Circocentri : ',circocentri)
    
    for i,l in zip(circocentri,nodes_coordinates):
        #angle = math.radians(120)
        #print('This is i',i)
        #print('This is l',l)
        for m in i:
            # print('This is m',m)
            dist = ((m[0][0] - l[1])**2 + (m[0][1]-l[2])**2) < rs**2
            # print('This is distance : ',dist, 'between',l[0],'and',m[2],'and',m[3])
            if dist == False :
                # print('These are the probable stuck nodes :',l[0],m[4],m[7])
                ang = math.degrees(math.atan2(m[6]-m[3], m[5]-m[2]) - math.atan2(m[9]-m[3], m[8]-m[2]))
                # print('This is the supposed angle',ang)
                if ang > 120:
                    #print('The node :',m[7],m[1],m[4], 'is a stuck node')
                    nodes_stuck[m[1]] = True
                    nodes_state[m[1]] = 1
    return
# The stuck nodes that it found are all on the boundary of the graph, it doesn't find any within the hole.

def is_left(a, b, c):
    # Compute the cross product of the vectors (a, b) and (a, c)
    # The z-component of the cross product will be positive if c is to the left of (a, b)
    # and negative if c is to the right of (a, b)
    # If the cross product is zero, the points are collinear
    cross_product = (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])
    if cross_product > 0:
        return True
    else:
        return False
    
def get_non_boundary_nodes(current_node, visited):
    # Initialize the set of non-boundary nodes
    non_boundary_nodes = []
    current_node_short = [current_node[0],current_node[1],current_node[2]]
    # Iterate over all nodes in the visited set
    for node in visited: #x,y,id
        # Check if the node is connected to the current node
        if node in current_node[3]:
            # Check if the node is inside the boundary
            is_inside = True
            for other_node in visited:
                if other_node != node and other_node != current_node_short and is_left(current_node_short, node, other_node):
                    is_inside = False
                    break

            # If the node is not inside the boundary, add it to the non-boundary nodes set
            if not is_inside:
                non_boundary_nodes.append(node[2])

    # Return the set of non-boundary nodes
    return non_boundary_nodes


def boundhole(stuck_nodes,objects):
    for i in zip(stuck_nodes.x,stuck_nodes.y,stuck_nodes.id,stuck_nodes.gg_neighbours):
    # Initialize the boundary and visited sets
        boundary = []
        visited = []

    # Add the starting node to the boundary set
        boundary.append(i)
        #print('This is the first boundary',boundary)
    # Iterate until the boundary set is empty
        while boundary:
        # Get the next node from the boundary set and add it to visited
            current_node = boundary.pop()
            visited.append([current_node[0],current_node[1],current_node[2]]) #x,y,id
            #print('This is visited',visited)
        # Find all neighbors of the current node that have not been visited
            for neighbor in current_node[3]: #x,y,id
                #print('These are the neighbours:', neighbor)
                if neighbor not in visited:
                    # Check if the neighbor is inside the boundary
                    is_inside = True
                    for node in boundary:
                        #print('This is node:',node)
                        if is_left(current_node, neighbor, node):
                            is_inside = False
                            break

                # If the neighbor is inside the boundary, add it to the boundary set
                    if is_inside:
                    # scorri tutti i nodi e appendi il nodo intero
                        for i in zip(objects.x,objects.y,objects.id,objects.gg_neighbours):
                            if i[2] == neighbor[2]:
                                boundary.append(i)
                                
            non_boundary = get_non_boundary_nodes(current_node, visited)
            print('This is non_boundary:', non_boundary)
            print('This is boundary before removal',boundary)
            boundary = [b for b in boundary if b[2] not in non_boundary]
            print('Result',boundary)

    # Return the list of nodes on the boundary of the hole
    #print('These should be the final visited', visited)
    for q in visited:
        objects.hole[q[2]]=True
    return list(visited)          
        

class msg(Hook):
    def __init__(self,cfg):
        # self.counter = 0
        pass

    def msg1(self,objects): # viene eseguito ad ogni thick

        pass

    def msg2(self,objects): # viene eseguito una volta sola all'inizio

        #intact_nodes = objects.loc['fault' == False]
        intact_nodes = objects[objects['fault']==False]
        adjacent_nodes = find_adjacent_nodes(intact_nodes)
        nodes_neighbours = find_neighbours(objects,adjacent_nodes)
        coordinates_sorted = sort_coordinates(objects)
        add_id_to_neighbours = add_id_to_neighours(objects)
        # At this point i have all the adjacent nodes for each node in anticlockwise order with id, x,y
        # Hole identification 
        # tent_rules = tent_rule(objects)
        add_last_node = add_first_neighbour_to_the_end(objects.ordered_neighbours)
        gabriel_graphs = gabriel_graph(objects)
        #add_last_node_gg = add_first_neighbour_to_the_end_gg(objects.gg_neighbours)
        nodes_coordinates = nodes_coordinates_id(objects)
        #circocentri = find_circocentri(objects.ordered_neighbours,nodes_coordinates)
        circocentri = find_circocentri_gg(objects.gg_neighbours,nodes_coordinates)
        # circocentri è [[(x,y del circocentro),nodo importante, nodo2, nodo1]]
        tent = tent_rule(circocentri,nodes_coordinates,objects.stuck,objects.state)
        stuck_node = objects[objects['state']==1]
        boundhole_algorithm = boundhole(stuck_node,objects) 
                

# Node logic, the node only knows about his state not the one of the others, actions repeated every tick
def node_logic(node):

    if node.state == 1: #if state ==  1 the node is a stuck node
        #boundhole_algorithm = boundhole(node)
        pass
    if node.state == 2:

        pass
    
    
    return node
