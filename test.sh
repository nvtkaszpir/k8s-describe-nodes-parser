#!/usr/bin/env bash

set -eux
python3 k8s_resources.py --input data/nodes-fake.txt >data/output.json
