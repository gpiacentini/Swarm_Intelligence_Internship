#!/bin/bash

RUNS=100
FAULT_PERC=(0.05 0.1 0.25)
PLATELETS=(53 55 63)
QUEUE=parallel-cpu


for i in ${!FAULT_PERC[@]}; do
    fault_perc=${FAULT_PERC[$i]}
    platelets=${PLATELETS[$i]}
    for j in $(seq 1 $RUNS); do
        CLEARML_QUEUE=$QUEUE python main.py \
        -cn single-hole \
        params.fault_perc=$fault_perc \
        params.errors.rab_dist_more=0.015 \
        params.errors.rab_angle=0.0872665 \
        init.platelets.nests=1 \
        init.platelets.nest.platelets=$platelets \
        scenario.ntb=[7] \
        clearml.tags=single-pfault
    done
done
