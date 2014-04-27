#!/bin/bash

virtualenv venv

# Xcode 5.1 compilation fix. See:
# http://bruteforce.gr/bypassing-clang-error-unknown-argument.html
export ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future

source ./venv/bin/activate && pip install -r requirements.txt
