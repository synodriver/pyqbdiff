"""
Copyright (c) 2008-2023 synodriver <diguohuangjiajinweijun@gmail.com>
"""
from qbdiff.backends.cffi._qbdiff import ffi, lib

QBERR_OK           = lib.QBERR_OK
QBERR_NOMEM        = lib.QBERR_NOMEM
QBERR_IOERR        = lib.QBERR_IOERR
QBERR_TRUNCPATCH   = lib.QBERR_TRUNCPATCH
QBERR_BADPATCH     = lib.QBERR_BADPATCH
QBERR_BADCKSUM     = lib.QBERR_BADCKSUM
QBERR_LZMAERR      = lib.QBERR_LZMAERR
QBERR_SAIS         = lib.QBERR_SAIS

def version() -> str:
    return ffi.string(lib.qbdiff_version()).decode()


def error(code: int) -> str:
    return ffi.string(lib.qbdiff_error(code)).decode()


def compute(old: bytes, new_: bytes, diff_file: str) -> int:
    # cdef int ret
    f = lib.fopen(diff_file.encode(), b"wb")
    if f == ffi.NULL:
        raise ValueError("can not open file")
    try:
        ret = lib.qbdiff_compute(
            ffi.from_buffer(old), ffi.from_buffer(new_), len(old), len(new_), f
        )
        if ret != lib.QBERR_OK:
            raise ValueError(
                f"Failed to create delta (error {ret}: {ffi.string(lib.qbdiff_error(ret)).decode()}"
            )
        return ret
    finally:
        lib.fflush(f)
        lib.fclose(f)


def patch(old: bytes, patch_: bytes, new_file: str) -> int:
    f = lib.fopen(new_file.encode(), b"wb")
    if f == ffi.NULL:
        raise ValueError("can not open file")
    try:
        ret = lib.qbdiff_patch(
            ffi.from_buffer(old), ffi.from_buffer(patch_), len(old), len(patch_), f
        )
        if ret != lib.QBERR_OK:
            raise ValueError(
                f"Failed to patch (error {ret}: {ffi.string(lib.qbdiff_error(ret)).decode()}"
            )
        return ret
    finally:
        lib.fflush(f)
        lib.fclose(f)
