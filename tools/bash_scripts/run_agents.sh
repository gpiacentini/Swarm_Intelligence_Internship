#!/bin/bash

RUNS=100
AGENTS=(10 15 20 25)
QUEUE=parallel-cpu

for agents in ${AGENTS[@]}; do
    for i in $(seq 1 $RUNS); do
        CLEARML_QUEUE=$QUEUE python main.py \
        -cn single-hole \
        init.platelets.nests=4 \
        init.platelets.nest.platelets=$agents \
        scenario.ntb=[7] \
        clearml.tags=single-agents
    done
done
