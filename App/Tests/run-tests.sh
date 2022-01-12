#!/bin/sh
python3 testswithdb.py
systemctl stop docker
python3 testwithoutdb.py
