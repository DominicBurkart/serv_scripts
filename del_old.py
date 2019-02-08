import os
import sys
from datetime import date

example_date = "2019-12-31"


def check_date(datestr: str) -> None:
    ''' validate that a given datestring corresponds to a valid date in the 2000-2100 century.'''
    assert len(datestr) == len(example_date)
    parts = datestr.split("-")
    assert len(parts) == 3
    d = date(year=int(parts[0]), month=int(parts[1]), day=int(parts[2]))
    assert 2000 < d.year and d.year < 2100


def get_date(fname: str) -> str:
    '''Takes the datestring (format: yyyy-mm-dd) from a filename (format: [topic]yyyy-mm-dd.tsv)'''
    i = fname.index(".")
    assert i > 0
    out = fname[i - len(example_date): i]
    check_date(out)
    return out


if __name__ == "__main__":
    print("DELETING OLD DATA FILES.")
    folder = sys.argv[1] if len(sys.argv) > 1 else "twitter_streams"
    fnames = map(lambda fname: os.path.join(folder, fname), os.listdir(folder))
    datemap = {}
    for fname in fnames:
        try:
            d = get_date(fname)
            if d in datemap:
                datemap[d].append(fname)
            else:
                datemap[d] = [fname]
        except AssertionError:
            print("INVALID FILENAME (IGNORED): {}".format(fname))
    latest = max(datemap.keys())
    for old_date in [d for d in datemap.keys() if d != latest]:
        for f in datemap[old_date]:
            os.remove(f)
    print("OLD DATA FILES DELETED.")
