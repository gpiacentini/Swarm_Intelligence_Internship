import hydra
import pandas as pd
import numpy as np
import random

 
from src.simulator import Simulator, RenderFunction, GlobalFunction, TickFunction, EventsFunction
from src.logger import GlobalLogger

from src.logic.controller.init import init_nodes, scale_params
from src.logic.controller.core import render_fn, node_logic, events_fn
from src.logic.common import get_move
from src.logic.controller.metrics import CoverageMetric
from src.scenario.generate import generate


@hydra.main(version_base=None, config_path="config", config_name="config")
def main(cfg):
    if cfg.seed == -1:
        cfg.seed = np.random.randint(0, 2**32-1)
    np.random.seed(cfg.seed)
    random.seed(cfg.seed)

    if cfg.log.stdout:
        from src.logger import StdoutLogger
        GlobalLogger.add_logger(logger=StdoutLogger())
    if cfg.log.clearml:
        from src.logger import ClearMLLogger
        GlobalLogger.add_logger(logger=ClearMLLogger(
            project=cfg.clearml.project,
            task=cfg.clearml.task,
            output_uri=cfg.clearml.output_uri,
            media_uri=cfg.clearml.media_uri,
            tags=cfg.clearml.tags,
            newtask=cfg.clearml.newtask,
            seed=cfg.seed,
        ))

    generated = None
    while generated is None:
        try:
            generated = generate(cfg)
        except:
            print("Failed generation, retrying...")
    
    GlobalLogger.log_media("init_network", generated["plots"]["init_network"])
    GlobalLogger.log_media("final_network", generated["plots"]["final_network"])

    scale_params(cfg, generated["scale_factor"])

    nodes = init_nodes(cfg, generated["nodes"])
   
    simulator = Simulator(cfg)

    simulator.add_objects(
        type="node",
        objects=nodes,
    )



    simulator.add_render_fn(function=RenderFunction(fn=render_fn))
    simulator.add_events_fn(function=EventsFunction(fn=events_fn))
    simulator.add_hook(CoverageMetric(cfg))
    

    simulator.add_tick_fn(
        target="node",
        function=TickFunction(
            fn=node_logic,
            backend="python",
            inputs=["boundary", "id", "fault"],
            outputs=["v", "w"],
            types=dict(
                range_and_bearing="object",
            )
        )
    )


    simulator.run(
        ticks=cfg.max_ticks,
        render=True,
        record=cfg.record,
        delete_recording=cfg.delete_recording,
        headless=cfg.headless,
        render_surface=cfg.world.size,
        render_background=cfg.world.background
    )

if __name__ == "__main__":
    main()