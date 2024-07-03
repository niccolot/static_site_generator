#!/usr/bin/bash

export PYTHONPATH=$(pwd)/src

python src/site_generator/main.py

cd public && python -m http.server 8888