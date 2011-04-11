#/usr/bin/env python

from numarray import *
from ppgplot import *

s602 = sin(pi/3) / 2
c602 = cos(pi/3) / 2

def drawtriangle (p1, p2, p3, i):
    if (i > 5) :
	return
    l = sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    pgmove(p1[0], p1[1])
    pgdraw(p2[0], p2[1])
    pgdraw(p3[0], p3[1])
    pgdraw(p1[0], p1[1])

    pgsci(1)
    drawtriangle(p1, [p1[0] + l/2, p1[1]], \
		 [p1[0] + l*c602, p1[1] + l*s602], i+1)
    pgsci(2)
    drawtriangle([p2[0] - l/2, p2[1]], p2, \
		 [p2[0] - l*c602, p2[1] + l*s602], i+1)
    pgsci(3)
    drawtriangle([p3[0] - l*c602, p3[1] - l*s602], \
		 [p3[0] + l*c602, p3[1] - l*s602], p3, i+1)


l = 1
p1 = [0,0]
p2 = [l,0]
p3 = [cos(pi/3), sin(pi/3)]

print p3

pgbeg('?')
pgask(1)
pgenv(0,1,0,1)
pgslw(5)
pgsci(1)


drawtriangle(p1,p2,p3,0)
pgend()


    
