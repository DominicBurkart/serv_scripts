#!/usr/bin/env bash

cd /home/dominic/shiny/hyperstream
python3 -c 'import generate_directory as gd; gd.remigrate_gzips("/home/dominic/shiny/hyperstream/all_gzips")'