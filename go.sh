#!/bin/bash
set -euo pipefail
shopt -s inherit_errexit

lint() {
    flake8 source/ccombine.py
    mypy --strict source/ccombine.py
}

tar() {
    local version="$(git describe --always --abbrev=20)"
    if [[ -z $version ]]; then
        return 1
    fi
    version="${version/#v/}"
    local folder="ccombine-$version"
    local tarball="$folder.tar"
    local zstdcmd="zstd --rm --force -q -10 -T0"

    git archive --verbose --prefix "${folder}/" --output "$tarball" @
    $zstdcmd "$tarball"
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
