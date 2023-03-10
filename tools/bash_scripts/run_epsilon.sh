#!/bin/bash

RUNS=100
EPSILONS=(0 0.1666 0.3333)
QUEUE=parallel-cpu

for epsilon in ${EPSILONS[@]}; do
    for i in $(seq 1 $RUNS); do
        CLEARML_QUEUE=$QUEUE python main.py \
        -cn single-hole \
        params.epsilon=$epsilon \
        clearml.tags=single-epsilon
    done
done

