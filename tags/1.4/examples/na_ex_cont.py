#/usr/bin/env python

from numarray import *
from ppgplot import *

# initialize ploting.
pgbeg("?",1,1)       # open ploting device
pgask(1)                 # wait for user to press a key before erasing.
pgenv(1,40,1,40)         # set axis ranges, and draw axes.
                         # label the plot.
pglab("x","y","z = cos(.3*sqrt(2*x) - .4*y/3)*cos(.4*x/3) + (x-y)/40.0")
pgiden()                 # put user-name and date on plot.

# calculate a suitable function.
surf = zeros([40,40],Float32)
for i in range(1,41):
    for j in range(1,41):
	surf[i-1,j-1] = cos(.3*sqrt(2*i) - .4*j/3)*cos(.4*i/3) + (i-j)/40.0
mns, mxs = min(ravel(surf)), max(ravel(surf))


# do the ploting.
pggray_s(surf)           # image map of the array surf.
pgsci(2)                 # change color index to 2 (red).
pgcont_s(surf,10)        # trace 10 contours on array surf.
pgsci(3)                 # set color index to 3 (green).
for i in range(10):      # label the contours.
    c = mns + i*((mxs - mns) / (10-1))
    pgconl_s(surf,c,str(i))
pgsci(1)                 # set colndx back to 1 (white)
	                 # plot a wedge to the right of the image.
pgwedg_s(max(ravel(surf)),min(ravel(surf)), "RG")

#close the plot.
pgend()

