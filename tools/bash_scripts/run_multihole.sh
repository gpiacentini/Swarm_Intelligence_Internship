#!/bin/bash

RUNS=300
QUEUE=parallel-cpu

for i in $(seq 1 $RUNS); do
    CLEARML_QUEUE=$QUEUE python main.py \
    -cn single-hole \
    init.platelets.nests=1 \
    init.platelets.nest.platelets=70 \
    scenario.ntb=[3,3,4] \
    clearml.tags=multihole-2
done
