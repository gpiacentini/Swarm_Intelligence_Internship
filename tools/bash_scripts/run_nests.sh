#!/bin/bash


RUNS=100
NESTS=(1 3 5)
AGENTS=(50 17 10)
QUEUE=parallel-cpu

for i in ${!NESTS[@]}; do
    nests=${NESTS[$i]}
    agents=${AGENTS[$i]}
    for j in $(seq 1 $RUNS); do
        CLEARML_QUEUE=$QUEUE python main.py \
        -cn single-hole \
        init.platelets.nests=$nests \
        init.platelets.nest.platelets=$agents \
        scenario.ntb=[7] \
        clearml.tags=single-nests-2
    done
done
