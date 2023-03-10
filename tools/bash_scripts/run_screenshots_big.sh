#!/bin/bash

RUNS=150
QUEUE=parallel-cpu

for i in $(seq 1 $RUNS); do
    CLEARML_QUEUE=$QUEUE python main.py \
    -cn screenshots \
    max_ticks=1500 \
    init.platelets.nests=2 \
    init.platelets.nest.platelets=35 \
    scenario.ntb=[3,3,4] \
    network.epsilon=5 \
    network.x_limits=[0,500] \
    network.y_limits=[0,500] \
    network.n_nodes=200 \
    clearml.tags=multihole-screenshots-big-3
done
