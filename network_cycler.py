import itertools
import os
import shutil
import subprocess
import time
from typing import NamedTuple

import pandas as pd

collection_file_base_name = "cycle_collection_2019" # don't include filetype (i.e. ".csv").
jar_file = "TwitterUserFollowersFriends.jar" # should be in base_dir
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
    log_file: str
    errored: bool


def run_collection(id: str) -> Collection:
    start_time = time.time()
    log_file = "{}__{}.txt".format(time.strftime("%Y-%m-%d_%H-%M-%S"), id)
    dir_before = os.listdir(os.curdir)

    # run collection
    resp = subprocess.run("java -Xmx12g -jar {} {} > {}".format(jar_file, id, log_file), shell=True)
    end_time = time.time()

    # get output directory
    new_files_about_user = [f for f in os.listdir(os.curdir) if f not in dir_before and "_{}_".format(id) in f]
    assert len(new_files_about_user) == 1  # weird race case. Nothing else should be writing to this directory.
    assert os.path.isdir(new_files_about_user[0])
    out_dir = new_files_about_user[0]

    return Collection(
        out_dir=out_dir,
        start_time=start_time,
        end_time=end_time,
        duration=end_time - start_time,
        root_id=id,
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
