#!/usr/bin/env bash
set -euo pipefail
shopt -s inherit_errexit

version=1.5.0
dir="zstd-$version"
tarball="v$version.tar.gz"
url="https://github.com/facebook/zstd/archive/refs/tags/v$version.tar.gz"

log() {
    printf '%s\n' "$*"
}

download_tar() {
    log "Downloading tarball to $tarball"
    curl -fRLO "$url"
}

extract_tar() {
    log "Extracting tarball into $dir"
    tar -xf "$tarball"
}

copy_scripts() {
    cp combine.sh "$dir"/build/single_file_libs/
    cp ../source/ccombine.py "$dir"/build/single_file_libs/
}

run() (
    cd "$dir"/build/single_file_libs/
    hyperfine -w 1 -m 3 'python3 ccombine.py -r ../../lib/ zstd-in.c >ztest1.c'
    hyperfine -w 1 -m 3 'busybox ash -e combine.sh -r ../../lib/ -o ztest2.c zstd-in.c'
    hyperfine -w 1 -m 3 'sh -e combine.sh -r ../../lib/ -o ztest3.c zstd-in.c'
    rm -- ztest?.c
)

if [[ ! -f $tarball ]]; then
    download_tar
fi

if [[ ! -d $dir ]]; then
    extract_tar
fi

copy_scripts
run
