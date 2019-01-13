import random
import shutil
import os

from del_old import *


def test_check_date() -> None:
    goods = [
        "2018-10-09",
        "2019-12-31",
        "2017-01-01",
    ]
    bads = [
        "2018-13-13",
        "2018-03-31"
        "01-02-2019",
        "22019-01-02",
        "2019-02-2",
        "2018-2-3-3"
    ]
    for g in goods:
        check_date(g)
    for b in bads:
        try:
            check_date(b)
        except (AssertionError, ValueError):
            pass
        else:
            raise AssertionError("Bad input ({}) did not error as expected.".format(b))


def test_get_date() -> None:
    good_fnames = [
        "lgbtq2019-01-12.tsv",
        "USA2019-01-13.tsv",
        "ab1232017-09-20.tsv",
        "ab1232018-12-01.tsv.file"
    ]
    bad_fnames = [
        "USA019-01-13.tsv",
        "lgbtq2019-01-12tsv"
    ]
    for g in good_fnames:
        assert type(get_date(g)) == str
    for b in bad_fnames:
        try:
            get_date(b)
        except (AssertionError, ValueError):
            pass
        else:
            raise AssertionError("Bad input ({}) did not error as expected.".format(b))


def setup_fake_dir(fnames) -> str:
    d = "__del_old_test_tempdir__"
    folder = os.path.join(os.curdir, d)
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)
    for f in fnames:
        with open(os.path.join(folder, f), "w") as fileout:
            fileout.write(str(random.randint(0, 1000000)))
    return folder


def check_and_delete_fake_dir(folder, expected) -> bool:
    actual = os.listdir(folder)
    shutil.rmtree(folder)
    return actual == expected


def test_del_old() -> None:
    good_fnames = ['presidency2019-01-06.tsv', 'lgbtq2019-01-06.tsv', 'homo_slurs2019-01-06.tsv', 'islam2019-01-06.tsv',
                   'healthcare2019-01-06.tsv', 'terrorist_terrorism2019-01-06.tsv', 'social_movements2019-01-06.tsv',
                   'healthcare2019-01-07.tsv', 'social_movements2019-01-07.tsv', 'presidency2019-01-07.tsv',
                   'lgbtq2019-01-07.tsv',
                   'islam2019-01-07.tsv', 'terrorist_terrorism2019-01-07.tsv', 'homo_slurs2019-01-07.tsv',
                   'healthcare2019-01-08.tsv',
                   'presidency2019-01-08.tsv', 'lgbtq2019-01-08.tsv', 'USA2019-01-08.tsv',
                   'terrorist_terrorism2019-01-08.tsv',
                   'social_movements2019-01-08.tsv', 'islam2019-01-08.tsv', 'homo_slurs2019-01-08.tsv',
                   'presidency2019-01-09.tsv',
                   'homo_slurs2019-01-09.tsv', 'healthcare2019-01-09.tsv', 'islam2019-01-09.tsv',
                   'terrorist_terrorism2019-01-09.tsv',
                   'social_movements2019-01-09.tsv', 'lgbtq2019-01-09.tsv', 'presidency2019-01-10.tsv',
                   'lgbtq2019-01-10.tsv',
                   'islam2019-01-10.tsv', 'homo_slurs2019-01-10.tsv', 'healthcare2019-01-10.tsv',
                   'terrorist_terrorism2019-01-10.tsv',
                   'social_movements2019-01-10.tsv', 'healthcare2019-01-11.tsv', 'presidency2019-01-11.tsv',
                   'lgbtq2019-01-11.tsv',
                   'terrorist_terrorism2019-01-11.tsv', 'islam2019-01-11.tsv', 'homo_slurs2019-01-11.tsv',
                   'social_movements2019-01-11.tsv', 'lgbtq2019-01-12.tsv', 'USA2019-01-12.tsv',
                   'presidency2019-01-12.tsv',
                   'France2019-01-12.tsv', 'islam2019-01-12.tsv', 'healthcare2019-01-12.tsv',
                   'homo_slurs2019-01-12.tsv',
                   'terrorist_terrorism2019-01-12.tsv', 'social_movements2019-01-12.tsv', 'France2019-01-13.tsv',
                   'presidency2019-01-13.tsv', 'USA2019-01-13.tsv', 'lgbtq2019-01-13.tsv', 'islam2019-01-13.tsv',
                   'healthcare2019-01-13.tsv', 'social_movements2019-01-13.tsv', 'terrorist_terrorism2019-01-13.tsv',
                   'homo_slurs2019-01-13.tsv']
    folder = setup_fake_dir(good_fnames)
    check_and_delete_fake_dir(folder, ['France2019-01-13.tsv',
                                       'presidency2019-01-13.tsv', 'USA2019-01-13.tsv', 'lgbtq2019-01-13.tsv',
                                       'islam2019-01-13.tsv',
                                       'healthcare2019-01-13.tsv', 'social_movements2019-01-13.tsv',
                                       'terrorist_terrorism2019-01-13.tsv',
                                       'homo_slurs2019-01-13.tsv'])
