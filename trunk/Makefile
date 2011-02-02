#
# For developers only
#
# Use this Makefile if you are doing development work on "ppgplot"
# itself. Its advantage compared to doing "python setup.py ..." is
# that "make" and "make clean" are much shorter to type. Also the
# default rule installs everything inside the source tree, (under
# "ppgplot-x.y/ppgplot/") so that you don't have to have root access,
# or have to pollute system-wide directories with stuff that are still
# under development.
#

PYTHON=python2.3

.PHONY : all install clean rebuild reinstall

all:
	$(PYTHON) setup.py install --install-lib=.
	ln -fs ../ppgplot examples/ppgplot 

install:
	$(PYTHON) setup.py install 

clean:
	$(PYTHON) setup.py clean --all
	rm -f MANIFEST
	rm -rf ./dist
	rm -rf ./ppgplot
	rm -f ./examples/ppgplot
	rm -f *~
	rm -f \#*\#
	rm -f ./doc/*~
	rm -f ./doc/\#*\#
	rm -f ./src/*~
	rm -f ./src/\#*\#
	rm -f ./examples/*~
	rm -f ./examples/\#*\#

rebuild: clean all

reinstall: clean install

sdist: clean
	$(PYTHON) setup.py sdist

