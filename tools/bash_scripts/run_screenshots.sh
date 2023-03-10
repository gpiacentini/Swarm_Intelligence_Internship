#!/bin/bash

RUNS=150
QUEUE=parallel-cpu

for i in $(seq 1 $RUNS); do
    CLEARML_QUEUE=$QUEUE python main.py \
    -cn screenshots \
    init.platelets.nests=3 \
    init.platelets.nest.platelets=24 \
    scenario.ntb=[3,3,4] \
    clearml.tags=multihole-screenshots-3_24
done

for i in $(seq 1 $RUNS); do
    CLEARML_QUEUE=$QUEUE python main.py \
    -cn screenshots \
    init.platelets.nests=5 \
    init.platelets.nest.platelets=14 \
    scenario.ntb=[3,3,4] \
    clearml.tags=multihole-screenshots-5_14
done
