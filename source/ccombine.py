#!/usr/bin/env python3
#
# © 2020 Aman Verma <https://aman.raoverma.com/contact.html>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

import argparse as ap
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List, Set

__version__ = "0.1.2"


@dataclass
class Options:
    input_file: Path
    root: List[Path]
    exclude: Set[str]
    keep: Set[str]
    include_pragma_once: bool = False


def main(arguments: List[str] = sys.argv[1:]) -> None:
    parser = ap.ArgumentParser(
        description=(
            "Processes a C/C++ source file, recursively inlining any local includes."
        ),
        add_help=False,
    )
    parser.add_argument("input_file", action="store", type=Path)
    parser.add_argument(
        "-r",
        "--root",
        action="append",
        type=Path,
        help="Include search path, can be repeated.",
        default=[],
    )
    parser.add_argument(
        "-x",
        "--exclude",
        action="append",
        help="Header to exclude from inlining, can be repeated.",
        default=[],
    )
    parser.add_argument(
        "-k",
        "--keep",
        action="append",
        help="Header to exclude from inlining but keep the include, can be repeated.",
        default=[],
    )
    parser.add_argument(
        "-p",
        "--include-pragma-once",
        action="store_true",
        help='Keep any "#pragma once" directives (removed by default).',
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=ap.SUPPRESS,
        help="Show this help message and exit.",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="ccombine " + __version__,
        help="Show program's version number and exit.",
    )

    args = parser.parse_args(arguments)
    opts = Options(
        input_file=args.input_file,
        root=[p.resolve(strict=True) for p in args.root],
        exclude=set(args.exclude),
        keep=set(args.keep),
        include_pragma_once=args.include_pragma_once,
    )
    process(opts)


def process(opts: Options) -> None:
    already_included: Set[Path] = set()
    process_file(opts.input_file, already_included, opts)


def process_file(file: Path, already_included: Set[Path], opts: Options) -> None:
    if not file.is_file():
        sys.exit(f"ERROR: '{file}' is not a file.")

    with file.open("r", encoding="utf-8", newline=None) as f:
        for line in f:
            process_line(
                line.rstrip("\n"),
                file.parent.resolve(strict=True),
                already_included,
                opts,
            )


re_inc_local = re.compile(r'\s*#\s*include\s*"(.+?)"')
re_pragma_once = re.compile(r"\s*#\s*pragma\s*once")


def process_line(
    line: str, working_dir: Path, already_included: Set[Path], opts: Options
) -> None:
    match_inc = re_inc_local.match(line)
    if match_inc is None:
        if re_pragma_once.match(line) is None or opts.include_pragma_once:
            print(line)
        return

    inc = match_inc.group(1)
    if inc in opts.exclude:
        print(f"#error Using excluded file {inc}")
        warn(f"Using excluded file {inc}. #error directive inserted.")
        return

    resolved_inc = resolve_include((working_dir, *opts.root), inc)
    if resolved_inc in already_included:
        print(f"/* === skipping file {inc} === */")
        return

    already_included.add(resolved_inc)
    if inc in opts.keep:
        log(f"Not inlining {inc}")
        print(f"/* === not inlining {inc} === */")
        print(line)
        return

    print(f"/* === start inlining {inc} === */")
    log(f"Inlining {inc}")
    process_file(resolved_inc, already_included, opts)
    print(f"/* === end inlining {inc} === */")


def resolve_include(dirs: Iterable[Path], filename: str) -> Path:
    for dir in dirs:
        possible_file = dir / filename
        if possible_file.is_file():
            return possible_file.resolve(strict=True)
    sys.exit(f"Couldn't find included file '{filename}'")


def log(msg: Any) -> None:
    print("INFO:", msg, file=sys.stderr)


def warn(msg: Any) -> None:
    print("WARNING:", msg, file=sys.stderr)


if __name__ == "__main__":
    main()
