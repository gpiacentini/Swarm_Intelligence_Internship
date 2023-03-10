#!/bin/sh

# plot coverage for epsilons

python -m scripts.download-results --tag single-epsilon
python -m scripts.plot-series --results ./results/single-epsilon.feather --series coverage_coverage --group Hydra/params.epsilon
python -m scripts.plot-series --results ./results/single-epsilon.feather --series bound_agents_bound_agents --group Hydra/params.epsilon
