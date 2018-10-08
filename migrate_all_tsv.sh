#!/usr/bin/env bash

cd /home/dominic/shiny/hyperstream
python3 -c 'import generate_directory as gd; gd.migrate_everything("/home/dominic/shiny/hyperstream/all_gzips")'