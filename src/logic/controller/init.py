import math
import pandas as pd
import numpy as np

def init_nodes(cfg, nodes, init_id=0):
    ret = []
    for i, node in enumerate(nodes):
        ret.append(dict(
            id=init_id+i,
            x=node.x,
            y=node.y,
            heading=node.heading,
            v=0.0,
            w=0.0,
            state = 0,
            stuck = False,
            neighbours = [],
            ordered_neighbours =[],
            gg_neighbours = [],

            fault=bool(node.fault),
            boundary=bool(node.boundary),
            communication_radius=cfg.params.rc[0],
            sensing_radius=cfg.params.rs[0]
        ))
    return pd.DataFrame(ret)


def scale_params(cfg, scale_factor):
    scale_factor = float(scale_factor)

    cfg.params.rs[0] /= scale_factor
    cfg.params.rs[1] /= scale_factor

    cfg.params.rc[0] /= scale_factor
    cfg.params.rc[1] /= scale_factor

    cfg.params.driving_speed_cruise /= scale_factor
    cfg.params.errors.rab_dist_more *= scale_factor