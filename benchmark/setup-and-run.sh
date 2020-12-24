#!/usr/bin/env bash
set -euo pipefail
shopt -s inherit_errexit

version=1.4.8
dir="zstd-${version}"
tarball="${dir}.tar.zst"
url="https://github.com/facebook/zstd/releases/download/v${version}/${tarball}"

log() {
    printf '%s\n' "$*"
}

download_tar() {
    log "Downloading tarball to $tarball"
    if command -v aria2c >/dev/null; then
        aria2c -q "$url"
    else
        curl -fLO "$url"
    fi
}

extract_tar() {
    log "Extracting tarball into $dir"
    tar -xf "$tarball"
}

copy_scripts() {
    cp combine.sh "$dir"/contrib/single_file_libs/
    cp ../source/ccombine.py "$dir"/contrib/single_file_libs/
}

run() (
    cd "$dir"/contrib/single_file_libs/
    hyperfine -w 1 -m 3 'python3 ccombine.py -r ../../lib/ zstd-in.c >ztest3.c'
    hyperfine -w 1 -m 3 'busybox ash combine.sh -r ../../lib/ -o ztest1.c zstd-in.c'
    hyperfine -w 1 -m 3 'sh combine.sh -r ../../lib/ -o ztest2.c zstd-in.c'
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
