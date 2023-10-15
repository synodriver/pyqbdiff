# cython: language_level=3
# cython: cdivision=True
from libc.stdint cimport uint8_t
from libc.stdio cimport FILE, fclose, fflush, fopen

from qbdiff.backends.cython cimport qbdiff
from qbdiff.backends.cython.qbdiff cimport (qbdiff_compute, qbdiff_error,
                                            qbdiff_patch, qbdiff_version)

QBERR_OK           = qbdiff.QBERR_OK
QBERR_NOMEM        = qbdiff.QBERR_NOMEM
QBERR_IOERR        = qbdiff.QBERR_IOERR
QBERR_TRUNCPATCH   = qbdiff.QBERR_TRUNCPATCH
QBERR_BADPATCH     = qbdiff.QBERR_BADPATCH
QBERR_BADCKSUM     = qbdiff.QBERR_BADCKSUM
QBERR_LZMAERR      = qbdiff.QBERR_LZMAERR
QBERR_SAIS         = qbdiff.QBERR_SAIS


cdef extern from "Python.h":
    const char *PyUnicode_AsUTF8(object u)

cpdef inline str version():
    return (<bytes>qbdiff_version()).decode()

cpdef inline str error(int code):
    return (<bytes>qbdiff_error(code)).decode()

cpdef inline int compute(const uint8_t[::1] old, const uint8_t[::1] new_, str diff_file) except -1:
    cdef int ret
    cdef FILE* f = fopen(PyUnicode_AsUTF8(diff_file),"wb")
    if f==NULL:
        raise ValueError("can not open file")
    try:
        with nogil:
            ret = qbdiff_compute(&old[0],&new_[0],<size_t>old.shape[0], <size_t>new_.shape[0], f)
        if ret != qbdiff.QBERR_OK:
            raise ValueError(f"Failed to create delta (error {ret}: {(<bytes>qbdiff_error(ret)).decode()}")
        return ret
    finally:
        fflush(f)
        fclose(f)

cpdef inline int patch(const uint8_t[::1] old, const uint8_t[::1] patch_, str new_file) except -1:
    cdef int ret
    cdef FILE* f = fopen(PyUnicode_AsUTF8(new_file),"wb")
    if f==NULL:
        raise ValueError("can not open file")
    try:
        with nogil:
            ret = qbdiff_patch(&old[0],&patch_[0],<size_t>old.shape[0], <size_t>patch_.shape[0], f)
        if ret != qbdiff.QBERR_OK:
            raise ValueError(f"Failed to patch (error {ret}: {(<bytes>qbdiff_error(ret)).decode()}")
        return ret
    finally:
        fflush(f)
        fclose(f)
