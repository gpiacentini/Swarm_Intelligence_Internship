#!/bin/bash


RUNS=100
NTB=(1 4 7 10 15)
AGENTS=(5 25 50 75 125)
QUEUE=parallel-cpu

for i in ${!NTB[@]}; do
    ntb=${NTB[$i]}
    agents=${AGENTS[$i]}
    for j in $(seq 1 $RUNS); do
        CLEARML_QUEUE=$QUEUE python main.py \
        -cn single-hole \
        init.platelets.nests=1 \
        init.platelets.nest.platelets=$agents \
        scenario.ntb=[$ntb] \
        clearml.tags=single-dimension-2
    done
done
