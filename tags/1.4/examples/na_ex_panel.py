#/usr/bin/env python

from numarray import *
from ppgplot import *

def fixenv (xrange=[0,1], yrange=[0,1], fname="none", ci = 2):
                              # set axis ranges.
    pgswin(xrange[0],xrange[1],yrange[0],yrange[1])     
    pgsci(ci)                # set color index.
    pgbox()                  # draw axes. 
    pgsci(1)                 # back to color index 1 (white)
    pglab("x","y",fname)     # label the plot

    
# initialize ploting.
pgbeg("?",2,2)       # open ploting device (2x2 pannels)
pgiden()                 # put user-name and date on plot.
pgask(1)                 # wait for user to press a key before erasing.

# calculate some suitable functions.
x = arange(0.01,6*pi,0.1)
y = zeros([2,2,x.shape[0]],Float64)
label = zeros([2,2],PyObject)
y[0,0] = sin(2*x)/x
label[0,0] = "sin(2*x)/x"
y[1,0] = sin(2*x)
label[1,0] = "sin(2*x)"
y[0,1] = x*sin(2*x)
label[0,1] = "x*sin(2*x)"
y[1,1] = sin(x) + sin(2*x) + sin(3*x)
label[1,1] = "sin(x) + sin(2*x) + sin(3*x)"

# do the plotting
for i in range(2):
    for j in range(2):
	pgpanl(i+1,j+1)
	fixenv([0.0,6*pi],[min(y[i,j]),max(y[i,j])],label[i,j], i*2+j+2)
	pgslw(6);          # set line-width to 6/201.
	pgsls(i*2+j+1)     # set the line style.
	pgline(x,y[i,j])   # plot the line.
	pgsls(1);          # recall line-style
	pgslw(1);          # recall line-width

#close the plot.
pgend()

