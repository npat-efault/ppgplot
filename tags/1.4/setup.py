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
name = "ppgplot"

found_module = False

try:
    # Try to use the "numpy" module (1st option)
    # uncomment the following line to disable usage of numpy
    #raise ImportError
    from numpy.distutils.core import setup, Extension
    from numpy.distutils.misc_util import get_numpy_include_dirs
    make_extension = Extension
    include_dirs.extend(get_numpy_include_dirs())
    define_macros.append(('USE_NUMPY', None))
    undef_macros.append('USE_NUMARRAY')
    print >>sys.stderr, "using numpy..."
    found_module = True
    # uncommenting the following line retains any previous ppgplot
    # package and installs this numpy-compatible version as
    # the package ppgplot_numpy
    #name = "ppgplot_numpy"
except ImportError:
    pass

if not found_module:
    try:
	# Try to use the "numarray" module (2nd option)
	# uncomment the following line to disable usage of numarray
	#raise ImportError
	from distutils.core import setup
	from numarray.numarrayext import NumarrayExtension
	make_extension = NumarrayExtension
	define_macros.append(('USE_NUMARRAY', None))
	print >>sys.stderr, "using numarray..."
	found_module = True
	# uncommenting the following line retains any previous ppgplot
	# package and installs this numpy-compatible version as
	# the package ppgplot_numpy
	#name = "ppgplot_numarray"
    except ImportError:
	pass

if not found_module:
    try:
	# Try to use the "Numeric" module (3rd option)
	# uncomment the following line to disable usage of Numeric
	#raise ImportError
	from distutils.core import setup, Extension
	make_extension = Extension
 	include_dirs.append(
	    os.path.join(get_python_inc(plat_specific=1), "Numeric"))
	undef_macros.append('USE_NUMARRAY')
	print >>sys.stderr, "using Numeric..."
	found_module = True
	# uncommenting the following line retains any previous ppgplot
	# package and installs this numpy-compatible version as
	# the package ppgplot_numpy
	#name = "ppgplot_Numeric"
    except ImportError:
	pass

if not found_module:
    raise Exception, "None of numpy, numarray or Numeric found"

if os.name == "posix":
    #libraries.append("png")
    libraries.append("X11")
    libraries.append("m")
    # comment out g2c if compiling with gfortran (typical nowadays)
    # you may still need this if using an earlier fortran compiler
    # libraries.append("g2c")
    library_dirs.append("/usr/X11R6/lib/")
    if os.environ.has_key("PGPLOT_DIR"):
        library_dirs.append(os.environ["PGPLOT_DIR"])
        include_dirs.append(os.environ["PGPLOT_DIR"])
    # locate Aquaterm dynamic library if running Mac OS X SCISOFT
    # (www.stecf.org/macosxscisoft/)
    elif os.environ.has_key("SCIDIR"):
	libraries.append("aquaterm")
        library_dirs.append(os.path.join(os.environ["SCIDIR"], 'lib'))
    else:
        print >>sys.stderr, "PGPLOT_DIR env var not defined!"
else:
    raise Exception, "os not supported"

ext_ppgplot = make_extension(name+'._ppgplot',
			[os.path.join('src', '_ppgplot.c')],
			include_dirs=include_dirs,
			libraries=libraries,
			library_dirs=library_dirs,
			define_macros=define_macros,
			extra_compile_args=extra_compile_args)



###################################################################
# the package
#

setup(name=name,
      version="1.4",
      description="Python / Numeric-Python bindings for PGPLOT",
      author="Nick Patavalis",
      author_email="npat@efault.net",
      url="http://code.google.com/p/ppgplot/",
      packages=[name],
      package_dir={name:'src'},
      ext_modules=[ext_ppgplot])
