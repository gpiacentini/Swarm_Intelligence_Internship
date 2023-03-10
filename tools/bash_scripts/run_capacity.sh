#!/bin/bash

RUNS=100
CAPACITY=(0.85 0.9 0.95 1.0)
QUEUE=parallel-cpu

for capacity in ${CAPACITY[@]}; do
    for i in $(seq 1 $RUNS); do
        CLEARML_QUEUE=$QUEUE python main.py \
        -cn single-hole \
        params.th_c=$capacity \
        init.platelets.nests=1 \
        init.platelets.nest.platelets=50 \
        scenario.ntb=[7] \
        clearml.tags=single-capacity-2
    done
done
