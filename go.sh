#!/bin/bash
set -eu
shopt -s inherit_errexit

lint() {
    flake8 source/ccombine.py
    mypy source/ccombine.py
}

help() { h; }
h() {
    echo "$0 <task> [args]"
    echo "Tasks:"
    compgen -A function | sed -E '/default/d' | cat -n
}

default() {
    lint "$@"
}

TIMEFORMAT="Task completed in %3lR"
time ${@:-default}
