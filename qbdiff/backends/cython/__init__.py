"""
Copyright (c) 2008-2023 synodriver <diguohuangjiajinweijun@gmail.com>
"""
from qbdiff.backends.cython._qbdiff import (
    QBERR_BADCKSUM,
    QBERR_BADPATCH,
    QBERR_IOERR,
    QBERR_LZMAERR,
    QBERR_NOMEM,
    QBERR_OK,
    QBERR_SAIS,
    QBERR_TRUNCPATCH,
    compute,
    error,
    patch,
    version,
)
