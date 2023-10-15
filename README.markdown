<h1 align="center"><i>✨ pyqbdiff ✨ </i></h1>

<h3 align="center">The python binding for <a href="https://github.com/kspalaiologos/qbdiff">qbdiff</a></h3>

[![pypi](https://img.shields.io/pypi/v/bzip3.svg)](https://pypi.org/project/qbdiff/)
![python](https://img.shields.io/pypi/pyversions/qbdiff)
![implementation](https://img.shields.io/pypi/implementation/qbdiff)
![wheel](https://img.shields.io/pypi/wheel/qbdiff)
![license](https://img.shields.io/github/license/synodriver/pyqbdiff.svg)
![action](https://img.shields.io/github/workflow/status/synodriver/pyqbdiff/build%20wheel)

### install
```bash
pip install qbdiff
```


### Usage
```python
from qbdiff import compute, patch, version, error

old = b"1234"
new_ = b"123456"
compute(old, new_, "diff_tmp.bin")
with open("diff_tmp.bin", "rb") as f:
    diff = f.read()
patch(old, diff, "new.bin")
with open("new.bin", "rb") as f:
    newf = f.read()
assert new_ == newf

```
- use ```QBDIFF_USE_CFFI``` env var to specify a backend

### Public functions
```python
QBERR_BADCKSUM: int
QBERR_BADPATCH: int
QBERR_IOERR: int
QBERR_LZMAERR: int
QBERR_NOMEM: int
QBERR_OK: int
QBERR_SAIS: int
QBERR_TRUNCPATCH: int

def version() -> str: ...
def error(code: int) -> str: ...
def compute(old: bytes, new_: bytes, diff_file: str) -> int: ...
def patch(old: bytes, patch_: bytes, new_file: str) -> int: ...
```

### Build
Two env var is needed to build, ```LIB``` and ```INCLUDE```. ```LIB``` is the path of liblzma.lib/liblzma.so,
and ```INCLUDE``` is the directory of ```lzma.h```

```bash
git submodule update --init --recursive
python setup.py sdist bdist_wheel --use-cython --use-cffi
```