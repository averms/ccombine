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
[nothings/single\_file\_libs][sfl]
and ["SQLite is really easy to compile"][je].

[sfl]: https://github.com/nothings/single_file_libs/#single-file-public-domainopen-source-libraries-with-minimal-dependencies
[je]: https://jvns.ca/blog/2019/10/28/sqlite-is-really-easy-to-compile/
[csh]: https://github.com/facebook/zstd/blob/69b8361b0c92b0f2cc145eea17b7ff930166ea9d/contrib/single_file_libs/combine.sh
