import itertools
import os
import shutil
import subprocess
import time
from typing import NamedTuple

import pandas as pd

collection_file_base_name = "cycle_collection_2019"  # todo. Does not include .csv
jar_file = "TwitterUserFollowersFriends.jar"  # todo.
base_dir = "network_collections"
log_directory = os.path.join(base_dir, "logs")
collection_file = os.path.join(base_dir, collection_file_base_name + ".csv")
backup_collection_file = os.path.join(base_dir, "backup_{}.csv".format(collection_file_base_name))


class Collection(NamedTuple):
    out_dir: str
    start_time: float
    end_time: float
    duration: float
    root_id: int
    root_followers: int
    total_collected: int
    log_file: str
    errored: bool


def run_collection(id: str) -> Collection:
    start_time = time.time()
    log_file = "{}__{}.txt".format(time.strftime("%Y-%m-%d_%H-%M-%S"), id)

    # run collection here
    resp = subprocess.run("java -Xmx12g -jar {} {} > {}".format(jar_file, id, log_file),
                          shell=True)  # todo. also this is a memory hog. pipe stuff to the log_file.
    out_dir = "todo"  # todo detect new folder with this ID

    end_time = time.time()
    return Collection(
        out_dir=out_dir,
        start_time=start_time,
        end_time=end_time,
        duration=end_time - start_time,
        root_id=id,
        root_followers=0,  # todo
        total_collected=0,  # todo
        log_file=log_file,
        errored=True if resp.returncode != 0 else False
    )


def save_record(c: Collection, df: pd.DataFrame) -> pd.DataFrame:
    df = df.append(df.from_records(c))
    df.to_csv(backup_collection_file, index=False)
    shutil.copy(backup_collection_file, collection_file)
    return df


if __name__ == "__main__":
    df = pd.read_csv(collection_file)
    for id in itertools.cycle(df.id.values):
        df = save_record(run_collection(id), df)
