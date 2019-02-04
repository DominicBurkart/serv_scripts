import os
import subprocess
import time
from typing import NamedTuple, List, TypeVar, Generator

import numpy as np
import pandas as pd

collection_file = os.path.join("yikes", "TODO") # todo
log_directory = "todo" # todo


class Collection(NamedTuple):
    start_time: np.float64
    end_time: np.float64
    duration: np.float64
    root_id: np.uint64
    root_followers: np.uint64
    total_collected: np.uint64
    log_file: str
    errored: bool


T = TypeVar['T']


def loop(vals: List[T]) -> Generator[T]:
    assert len(vals) > 0
    i: int = 0
    while True:
        yield vals[i]
        i = i + 1 if i < len(vals) else 0


def run_collection(id: str) -> Collection:
    start_time = time.time()
    log_file = "{}__{}".format(time.strftime("%Y-%m-%d_%H-%S"), id)

    # run collection here
    resp = subprocess.run("java -Xmx12g -jar [file]", shell=True)  # todo. also this is a memory hog. pipe stuff to the log_file.

    end_time = time.time()
    Collection(
        start_time=start_time,
        end_time=end_time,
        duration=end_time - start_time,
        root_id=np.uint64(id),
        root_followers=0,  # todo
        total_collected=0,  # todo
        log_file=log_file,
        errored=True if resp.returncode != 0 else False
    )


def save_record(c: Collection, df: pd.DataFrame) -> pd.DataFrame:
    df = df.append(df.from_records(c))
    df.to_csv(collection_file, index=False)
    return df


if __name__ == "__main__":
    df = pd.read_csv(collection_file)
    for id in loop(df.id):
        df = save_record(run_collection(id), df)
