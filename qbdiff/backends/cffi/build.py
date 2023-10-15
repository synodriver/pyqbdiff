"""
Copyright (c) 2008-2023 synodriver <diguohuangjiajinweijun@gmail.com>
"""
import os
import sys

from cffi import FFI

define_macros = []
if sys.platform.startswith("win"):
    extra_compile_args = ["-openmp:experimental"]
    extra_link_args = ["-openmp:experimental"]
    define_macros.append(("LIBQDIFF_PUBLIC_API", "__declspec(dllexport)"))
elif sys.platform.startswith("darwin"):
    os.system("brew install libomp")
    extra_compile_args = ["-Xpreprocessor", "-fopenmp"]
    extra_link_args = ["-L/usr/local/lib", "-lomp"]
else:
    extra_compile_args = ["-fopenmp"]
    extra_link_args = ["-fopenmp"]


ffibuilder = FFI()
ffibuilder.cdef(
    """
#define QBERR_OK 0
#define QBERR_NOMEM 1
#define QBERR_IOERR 2
#define QBERR_TRUNCPATCH 3
#define QBERR_BADPATCH 4
#define QBERR_BADCKSUM 5
#define QBERR_LZMAERR 6
#define QBERR_SAIS 7

int qbdiff_compute(const uint8_t * old, const uint8_t * new, size_t old_len, size_t new_len,
                                       FILE * diff_file);
int qbdiff_patch(const uint8_t * old, const uint8_t * patch, size_t old_len, size_t patch_len,
                                     FILE * new_file);
const char * qbdiff_version(void);
const char * qbdiff_error(int code);

FILE *fopen   (const char *filename, const char  *opentype);
int    fflush (FILE *stream);
int  fclose   (FILE *stream);
    """
)

source = """
#include "libqbdiff.h"
"""
c_sources = [
    "./dep/src/blake2b.c",
    "./dep/src/libqbdiff.c",
    "./dep/src/libsais.c",
    "./dep/src/libsais64.c",
]

ffibuilder.set_source(
    "qbdiff.backends.cffi._qbdiff",
    source,
    sources=c_sources,
    include_dirs=["./dep/include", os.getenv("INCLUDE", "")],
    define_macros=define_macros,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    extra_objects=[os.getenv("LIB", "")],
)

if __name__ == "__main__":
    ffibuilder.compile()
