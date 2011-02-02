from distutils.core import setup, Extension
from distutils.sysconfig import get_python_inc, get_python_lib
import os
import sys

###################################################################
# build the extension
#

define_macros = []
undef_macros = []
include_dirs = []
extra_compile_args = []
libraries = ["cpgplot", "pgplot"]
library_dirs = []

try:
    #
    # Try to use the "numarray" module
    #
    from numarray.numarrayext import NumarrayExtension
    # comment-out the previous line ("from numarray ..."), 
    # and comment-in the following to force the use of "Numeric"
    #raise ImportError
    make_extension = NumarrayExtension
    define_macros.append(('USE_NUMARRAY', None))
    print >>sys.stderr, "using numarray..."
except ImportError:
    #
    # If "numarray" is not available, default to "Numeric"
    #
    make_extension = Extension
    include_dirs.append(
        os.path.join(get_python_inc(plat_specific=1), "Numeric"))
    undef_macros.append('USE_NUMARRAY')
    print >>sys.stderr, "using Numeric..."

if os.name == "posix":
    libraries.append("png")
    libraries.append("X11")
    libraries.append("m")
    libraries.append("g2c")
    library_dirs.append("/usr/X11R6/lib/")
    if os.environ.has_key("PGPLOT_DIR"):
        library_dirs.append(os.environ["PGPLOT_DIR"])
        include_dirs.append(os.environ["PGPLOT_DIR"])
    else:
        print >>sys.stderr, "PGPLOT_DIR env var not defined!"
else:
    raise Exception, "os not supported"

ext_ppgplot = make_extension('ppgplot._ppgplot',
			[os.path.join('src', '_ppgplot.c')],
			include_dirs=include_dirs,
			libraries=libraries,
			library_dirs=library_dirs,
			define_macros=define_macros,
			extra_compile_args=extra_compile_args)



###################################################################
# the package
#

setup(name="ppgplot",
      version="1.3",
      description="Python / Numeric-Python bindings for PGPLOT",
      author="Nick Patavalis",
      author_email="npat@efault.net",
      url="http://efault.net/npat/hacks/ppgplot",
      
      packages=['ppgplot'],
      package_dir={'ppgplot':'src'},
      ext_modules=[ext_ppgplot])
