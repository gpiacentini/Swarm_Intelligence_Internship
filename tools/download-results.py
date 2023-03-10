import argparse
import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from clearml import Task
from functools import reduce

def process_task(task):
    params = task.get_parameters()
    scalars = task.get_reported_scalars()
    #hydra_conf = task.get_configuration_object("OmegaConf")
    
    params["task_id"] = task.id

    scalars_dfs = []
    for group in scalars:
        for series in scalars[group]:
            scalars_df = pd.DataFrame({
                "x": scalars[group][series]["x"],
                f"{group}_{series}": scalars[group][series]["y"]
            })
            scalars_df["x"] = scalars_df["x"].astype(int)
            scalars_df = scalars_df.set_index("x")

            upsample_df = pd.DataFrame({
                "x": np.arange(0, scalars_df.index.max()+1),
                f"{group}_{series}": np.nan
            })
            upsample_df["x"] = upsample_df["x"].astype(int)
            upsample_df = upsample_df.set_index("x")

            scalars_df = pd.merge(upsample_df, scalars_df, left_index=True, right_index=True, how="outer")
            scalars_df[f"{group}_{series}"] = scalars_df[f"{group}_{series}_y"]
            scalars_df = scalars_df[[f"{group}_{series}"]]

            scalars_df[f"{group}_{series}"] = scalars_df[f"{group}_{series}"].interpolate(method="linear")
            scalars_df[f"{group}_{series}"] = scalars_df[f"{group}_{series}"].interpolate(method="bfill")

            scalars_df = scalars_df.sort_index()            
            scalars_dfs.append(scalars_df)
        

    scalars_df = reduce(lambda df1, df2: pd.concat([df1, df2], axis=1), scalars_dfs)
    
    params = pd.DataFrame([params] * len(scalars_df))
    params.index = scalars_df.index
    df = pd.merge(params, scalars_df, left_index=True, right_index=True)
    
    return df


parser = argparse.ArgumentParser()

parser.add_argument("--project", type=str, default="giada-drones")
parser.add_argument("--task", type=str, default="giada-drones-training")
parser.add_argument("--tag", type=str, required=True)
parser.add_argument("--output-uri", type=str, default="s3://s3.galatolo.xyz:443/clearml")
parser.add_argument("--media-uri", type=str, default="s3://s3.galatolo.xyz:443/clearml-media")
parser.add_argument("--output-folder", type=str, default="./results")

args = parser.parse_args()

tasks = Task.get_tasks(
    project_name=args.project,
    task_name=args.task,
    allow_archived=False,
    tags=[args.tag],
    task_filter=dict(
        status=["completed"]
    )
)

'''
tasks = [
    Task.get_task(task_id="878838fb645d4fa98e371900cf727077"),
    Task.get_task(task_id="c39d22ea984e430ab88273f7a70c901c")
]
'''

dfs = []
for task in tqdm(tasks):
    print(task.id)
    dfs.append(process_task(task))

df = pd.concat(dfs)
df = df.reset_index()

os.makedirs(args.output_folder, exist_ok=True)
df.to_feather(os.path.join(args.output_folder, f"{args.tag}.feather"))