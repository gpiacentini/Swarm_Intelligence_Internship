import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--results", type=str, required=True)
parser.add_argument("--series", type=str, required=True)
parser.add_argument("--group", type=str, required=True)

args = parser.parse_args()

data = pd.read_feather(args.results)

sns.lineplot(
    x="x",
    y=args.series,
    hue=args.group,
    data=data
)

plt.show()