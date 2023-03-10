#!/bin/bash

CLEARML_QUEUE=parallel-cpu python main.py \
-cn screenshots \
seed=2979773206 \
max_ticks=1500 \
init.platelets.nests=2 \
init.platelets.nest.platelets=35 \
scenario.ntb=[3,3,4] \
network.epsilon=5 \
network.x_limits=[0,500] \
network.y_limits=[0,500] \
network.n_nodes=200 \
clearml.tags=multihole-screenshots-big-3-one
