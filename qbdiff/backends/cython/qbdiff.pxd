# cython: language_level=3
# cython: cdivision=True
from libc.stdint cimport uint8_t
from libc.stdio cimport FILE


cdef extern from "libqbdiff.h" nogil:
    int QBERR_OK
    int QBERR_NOMEM
    int QBERR_IOERR
    int QBERR_TRUNCPATCH
    int QBERR_BADPATCH
    int QBERR_BADCKSUM
    int QBERR_LZMAERR
    int QBERR_SAIS
    int qbdiff_compute(const uint8_t * old, const uint8_t * new_, size_t old_len, size_t new_len,
                       FILE * diff_file)
    int qbdiff_patch(const uint8_t * old, const uint8_t * patch, size_t old_len, size_t patch_len,
                     FILE * new_file)
    const char * qbdiff_version()
    const char * qbdiff_error(int code)