#!/bin/sh
set -eu
python -m pip install --disable-pip-version-check --no-cache-dir -r requirements.txt
exec python stream.py
