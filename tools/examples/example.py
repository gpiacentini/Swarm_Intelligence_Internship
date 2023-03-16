import pandas as pd
import numpy as np
import math
import random
import pygame


from collections import Counter
from src.simulator import Simulator, RenderFunction, GlobalFunction, TickFunction
from src.logic.common import get_move, range_and_bearing


INFLUENCE_RADIUS = 150
MAX_LINEAR_SPEED = 10
MAX_ANGULAR_SPEED = 1

def init(*, number, type):
    ret = []
    for i in range(0, number):
        ret.append(dict(
            id=i,
            x=np.random.uniform(100, 900),
            y=np.random.uniform(100, 900),
            v=np.random.uniform(0, MAX_LINEAR_SPEED) if type == "drone" else 0,
            w=np.random.uniform(-MAX_ANGULAR_SPEED, MAX_ANGULAR_SPEED) if type == "drone" else 0,
            heading=np.random.uniform(0, 2*math.pi) if type == "drone" else 0,
            level=-1,
            state=random.choice(["red", "green", "blue"]),
            gossip=0,
            fault=0,
            communication_radius=INFLUENCE_RADIUS,
            range_and_bearing=[]
        ))
    return pd.DataFrame(ret)


def render(*, window, objects):
    for idx, object in objects.iterrows():
        color = object["state"]
        position = object["x"], object["y"]
        if object["type"] == "node":
            pygame.draw.circle(window, color, position, INFLUENCE_RADIUS, 1)
        
        for rnb in object.range_and_bearing:
            start_x = object["x"]
            start_y = object["y"]

            
            

        pygame.draw.circle(window, color, position, 10 if object["type"] == "node" else 3)


def change_color(object):
    nodes = object.range_and_bearing[object.range_and_bearing[:, 1] == 0]
    max_count = Counter(nodes[:, 2]).most_common(1)
    if len(max_count) > 0:
        object.state = max_count[0][0]
    return object

def main():
    nodes = init(number=10, type="node")
    drones = init(number=50, type="drone")
   
    simulator = Simulator()

    simulator.add_objects(
        type="node",
        objects=nodes,
    )
    simulator.add_objects(
        type="drone",
        objects=drones,
    )

    simulator.add_render_fn(function=RenderFunction(fn=render))
    simulator.add_global_tick_fn(function=GlobalFunction(fn=range_and_bearing))
    
    simulator.add_tick_fn(
        target="drone",
        function=TickFunction(
            fn=get_move(1),
            backend="numba",
            inputs=["x", "y", "heading", "v", "w"],
            outputs=["x", "y", "heading"]
        )
    )

    simulator.add_tick_fn(
        target="node",
        function=TickFunction(
            fn=change_color,
            backend="dask",
            inputs=["range_and_bearing"],
            outputs=["state"],
            types=dict(
                range_and_bearing="object",
                state="str",
            )
        )
    )

    simulator.run(ticks=3000, render=True)


if __name__ == "__main__":
    main()