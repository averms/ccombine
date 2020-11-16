# ccombine

```
                          _______________________________
                        ( Single file libraries are good. )
                          -------------------------------
   _____                O
  /     \            o
  vvvvvvv  /|__/| o
     I   /O,O   |
     I /_____   |      /|/|
    E|/^ ^ ^ \  |    /00  |    _//|
     |^ ^ ^ ^ |W|   |/^^\ |   /oo |
      \m___m__|_|    \m_m_|   \mm_|
                  --- Duke Lee
```

`ccombine` is based on a script in the Zstd source called [`combine.sh`][csh]. I
rewrote it in Python because the original is very slow. The only change is a
better command-line interface.

It can be used to create an amalgamated distribution of your library for easy
embedding into another source tree. Some reasons to do this are outlined in
[nothings/stb][sfl] and ["SQLite is really easy to compile"][je].

You can install it by cloning and running `pip install .`. This will install a
script called `ccombine` into your Python environment. Alternatively, you can
simply run `source/ccombine/__init__.py` without installing anything. The only
requirement is the Python 3.7 standard library.

If you need 3.6 compatibility see the `py3.6_compat` branch.

[sfl]: https://github.com/nothings/stb#why-single-file-headers
[je]: https://jvns.ca/blog/2019/10/28/sqlite-is-really-easy-to-compile/
[csh]: https://github.com/facebook/zstd/blob/69b8361b0c92b0f2cc145eea17b7ff930166ea9d/contrib/single_file_libs/combine.sh
