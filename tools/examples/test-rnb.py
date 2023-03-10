import pandas as pd
import numpy as np
import math
import random
import pygame

from collections import Counter
from src.simulator import Simulator, RenderFunction, GlobalFunction, TickFunction
from src.logic.common import get_move, range_and_bearing


COMMUNICATION_RADIUS = 50
MAX_LINEAR_SPEED = 10
MAX_ANGULAR_SPEED = math.pi/10

def init(*, number):
    ret = []
    for i in range(0, number):
        ret.append(dict(
            id=i,
            x=np.random.uniform(100, 900),
            y=np.random.uniform(100, 900),
            v=np.random.uniform(0, MAX_LINEAR_SPEED),
            w=np.random.uniform(-MAX_ANGULAR_SPEED, MAX_ANGULAR_SPEED),
            heading=np.random.uniform(0, 2*math.pi),
            communication_radius=COMMUNICATION_RADIUS,
            range_and_bearing=[],
            fault=0,
            state=0,
            level=0,
            gossip=0

        ))
    return pd.DataFrame(ret)


def render(*, window, objects):
    for idx, object in objects.iterrows():
        color = "white"
        position = object["x"], object["y"]
        pygame.draw.circle(window, color, position, COMMUNICATION_RADIUS, 1)
    
        x, y = position
        angle = object.heading
        width = 10
        height = 15

        points = [
            (x, y - (height / 2)),
            (x - (width / 2), y + (height /2)),
            (x, y + (height / 4)),
            (x + (width / 2), y + (height / 2)),
            (x, y - (height / 2)),
            (x, y + (height / 4)),
        ]

        position = pygame.math.Vector2((x, y))
        rotated_points = [
            (pygame.math.Vector2(p) - position) \
            .rotate_rad(angle + math.pi/2) \
            for p in points
        ]

        translated_points = [(position + p) for p in rotated_points]

        pygame.draw.polygon(
            window,
            color,
            translated_points
        )

        '''
        for rnb in object.range_and_bearing:
            xr = object.x
            yr = object.y

            delta = (object.heading + rnb[6])%(2*math.pi)
            xp = xr + rnb[5]*math.cos(delta)
            yp = yr + rnb[5]*math.sin(delta)

            pygame.draw.line(window, "white", [xr, yr], [xp, yp])
        '''
        p = pygame.math.Vector2(object.x, object.y)
        for rnb in object.range_and_bearing:
            n = pygame.math.Vector2(rnb[5], 0).rotate_rad(rnb[6])

            rnb_point = p + n.rotate_rad(object.heading)

            pygame.draw.line(window, "white", p, rnb_point)

        #h = pygame.math.Vector2(10, 0).rotate_rad(object.heading)
        #pygame.draw.line(window, "red", p, p+h)
        pygame.draw.circle(window, color, position, 3)


def main():
    agents = init(number=100)
   
    simulator = Simulator()

    simulator.add_objects(
        type="agent",
        objects=agents,
    )


    simulator.add_render_fn(function=RenderFunction(fn=render))
    simulator.add_global_tick_fn(function=GlobalFunction(fn=range_and_bearing))

    simulator.add_tick_fn(
        target="agent",
        function=TickFunction(
            fn=get_move(1),
            backend="numba",
            inputs=["x", "y", "heading", "v", "w"],
            outputs=["x", "y", "heading"]
        )
    )

    simulator.run(ticks=3000, render_fps=10, render=True)


if __name__ == "__main__":
    main()