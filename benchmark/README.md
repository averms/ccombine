# Comparing ccombine.py and combine.sh

When I first ran `combine.sh`, it was painfully slow. So, I tried to improve
its performance by making it work with busybox ash. The result of that attempt
is in the `combine.sh` contained in this directory. However, it was still slow
and quite ugly so I wrote `ccombine.py`.

Benchmarking against the Zstd 1.4.8 source code, I got these results:

| Script and method             | Time in seconds |
|-------------------------------|-----------------|
| `combine.sh` with Bash        | 189             |
| `combine.sh` with busybox ash | 31              |
| `ccombine.py` with Python 3.9 | 1.4             |

In other words, `ccombine.py` is 135 times faster than the original
`combine.sh`.

You can try to reproduce these results by running `./setup-and-run.sh`. It
requires

- `curl` or `aria2`
- GNU tar or libarchive tar
- `hyperfine`
