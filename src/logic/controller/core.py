import numpy as np
import random
import pygame
import math
from src.logic.controller.render import render_nodes
from src.simulator import GlobalConfig

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



# Node logic, the node only know about his state not the one of the others, actions repeated every thick
def node_logic(node):
    return node
