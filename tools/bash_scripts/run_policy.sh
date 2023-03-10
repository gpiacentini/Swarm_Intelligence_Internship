#!/bin/bash

RUNS=100
POLICY=(anpm npma pmna closest random)
QUEUE=parallel-cpu

for policy in ${POLICY[@]}; do
    for i in $(seq 1 $RUNS); do
        CLEARML_QUEUE=$QUEUE python main.py \
        -cn single-hole \
        params.policy=$policy \
        init.platelets.nests=1 \
        init.platelets.nest.platelets=50 \
        scenario.ntb=[7] \
        clearml.tags=single-policy-2
    done
done
