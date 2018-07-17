from   __future__          import print_function
from   distutils.sysconfig import get_python_inc, get_python_lib 
import os, re, sys, functools

# distutils does not like unrecognized options but we'd like the user to be 
# able to indicate which numarray/numpy/Numeric *not* to try.
# So we just strip all these options from sys.argv (and remember them).
# I did look at 
#    https://stackoverflow.com/questions/677577/distutils-how-to-pass-a-user-defined-parameter-to-setup-py
# but that is not what is needed; we need to look at the command line /before/ setup(...) 
# actually executed.
partition    = lambda pred, lst: functools.reduce(lambda acc, elem: (acc[0]+[elem], acc[1]) if pred(elem) else (acc[0], acc[1]+[elem]), sys.argv, (list(), list()))
(ours, argv) = partition(re.compile(r'^--no-(numpy|numarray|numeric)$', re.I).match, sys.argv)
sys.argv     = argv


###################################################################
# build the extension
#

# The options and paths will be built dynamically below
define_macros        = []
undef_macros         = []
include_dirs         = []
library_dirs         = []
extra_compile_args   = []
extra_link_args      = []
libraries            = []
runtime_library_dirs = []
name                 = "ppgplot"
found_module         = False

try:
    # Try to use the "numpy" module (1st option)
    # Pass '--no-numpy' to disable using numpy
    if '--no-numpy' in ours:
        raise ImportError
    from numpy.distutils.core import setup, Extension
    from numpy.distutils.misc_util import get_numpy_include_dirs
    make_extension = Extension
    include_dirs.extend(get_numpy_include_dirs())
    define_macros.append(('USE_NUMPY', None))
    undef_macros.append('USE_NUMARRAY')
    print("using numpy...", file=sys.stderr)
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
        # '--no-numarray' to disable detection of this candidate
        if '--no-numarray' in ours:
            raise ImportError
        from distutils.core import setup
        from numarray.numarrayext import NumarrayExtension
        make_extension = NumarrayExtension
        define_macros.append(('USE_NUMARRAY', None))
        print("using numarray...", file=sys.stderr)
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
        # the pattern should be obvious by now
        if '--no-Numeric' in ours:
            raise ImportError
        from distutils.core import setup, Extension
        make_extension = Extension
        include_dirs.append(
            os.path.join(get_python_inc(plat_specific=1), "Numeric"))
        undef_macros.append('USE_NUMARRAY')
        print("using Numeric...", file=sys.stderr)
        found_module = True
        # uncommenting the following line retains any previous ppgplot
        # package and installs this numpy-compatible version as
        # the package ppgplot_numpy
        #name = "ppgplot_Numeric"
    except ImportError:
        pass

if not found_module:
    raise Exception("None of numpy, numarray or Numeric found")

if os.name == "posix":
    #libraries.append("png")
    libraries.append("X11")
    libraries.append("m")
    # comment out g2c if compiling with gfortran (typical nowadays)
    # you may still need this if using an earlier fortran compiler
    # libraries.append("g2c")
    for ld in filter(os.path.isdir, ["/usr/lib/x86_64-linux-gnu/", "/usr/X11R6/lib/"]):
        library_dirs.append(ld)

    # attempt to find libcpgplot under $PGPLOT_DIR - such that $PGPLOT_DIR can
    # be pointed at e.g. giza (http://giza.sourceforge.net/) On some systems
    # the original PGPLOT can be installed as a package, so the libs &cet end
    # up under "/usr/lib/", but some users may prefer to bind the ppgplot
    # extension to the giza implementation.
    #
    # In such a case, convincing the compiler, linker and runtime to choose using
    # the libraries &cet from a non-standard path takes a bit more effort but can easily be done.
    #
    # Note: the alternative solution is to de-install the system PGPLOT but there are other
    #       (mainly astronomical) utilities who depend on PGPLOT and as such there is a need
    #       for both giza and PGPLOT to co-exist on the same system
    #
    #
    # The code below instruments the compiling+linking of the ppgplot extension
    # such that *IFF* libcpgplot.so is found somewhere under $PGPLOT_DIR it
    # will be 'hard linked' against it and instruct the linker to add the
    # dynamic library path into the shared library(ies). This means the user
    # will not have to set their LD_LIBRRARY_PATH and loading of the
    # _ppgplot.so module will 'just work' (famous last words)
    pgplotlibs = None
    pgplotdir  = os.environ["PGPLOT_DIR"] if "PGPLOT_DIR" in os.environ else None
    if pgplotdir is not None:
        if not os.path.isdir(pgplotdir):
            raise RuntimeError("$PGPLOT_DIR [{0}] is not a directory".format(pgplotdir))
        for (path, _, files) in os.walk( pgplotdir ):
            if 'libcpgplot.so' in files:
                pgplotlibs = path
                break
    # locate Aquaterm dynamic library if running Mac OS X SCISOFT
    # (www.stecf.org/macosxscisoft/)
    elif 'SCIDIR' in os.environ:
        libraries.append("aquaterm")
        library_dirs.append(os.path.join(os.environ["SCIDIR"], 'lib'))
    else:
        print("PGPLOT_DIR env var not defined, hoping libcpgplot is in system path(s)", file=sys.stderr)

    # if we found pgplotlibs, make sure the extension is linked against /them/
    if pgplotlibs is not None:
        # add the libraries by path and tell compiler/linker to include rpath
        extra_link_args.append( "-Wl,-rpath={0}".format(pgplotlibs) )
        extra_link_args += map(functools.partial(os.path.join, pgplotlibs), ["libcpgplot.so", "libpgplot.so"])
        runtime_library_dirs.append( pgplotlibs )
        # pgplotlibs can not be None if pgplotdir is not a directory so the following can be
        # executed unconditionally
        include_dirs       += [os.path.join(pgplotdir, "include")]
    else:
        # add "-lcpgplot -lpgplot" and hope for the best
        libraries += ["cpgplot", "pgplot"]
else:
    raise Exception("os not supported")

ext_ppgplot = make_extension(name+'._ppgplot',
            [os.path.join('src', '_ppgplot.c')],
            include_dirs=include_dirs,
            libraries=libraries,
            library_dirs=library_dirs,
            define_macros=define_macros,
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
            runtime_library_dirs=runtime_library_dirs)



###################################################################
# the package
#

setup(name=name,
      version="1.4",
      description="Python / Numeric-Python bindings for PGPLOT",
      author="Nick Patavalis",
      author_email="npat@efault.net",
      url="http://code.google.com/p/ppgplot/ https://github.com/haavee/ppgplot",
      packages=[name],
      package_dir={name:'src'},
      ext_modules=[ext_ppgplot])
