from numpy import *
import numexpr as ne
 
def mandel(n, m, itermax, xmin, xmax, ymin, ymax):
    ix, iy = mgrid[0:n, 0:m]
    x = linspace(xmin, xmax, n)[ix]
    y = linspace(ymin, ymax, m)[iy]
    c = x+complex(0,1)*y
    del x, y # save a bit of memory, we only need z
    img = zeros(c.shape, dtype=int)
    ix.shape = n*m
    iy.shape = n*m
    c.shape = n*m
    z = copy(c)
    for i in xrange(itermax):
        if not len(z): break # all points have escaped
        multiply(z, z, z)
        add(z, c, z)
        rem = abs(z)>2.0
        img[ix[rem], iy[rem]] = i+1
        rem = -rem
        z = z[rem]
        ix, iy = ix[rem], iy[rem]
        c = c[rem]
    return img
 
def nemandel(n, m, itermax, xmin, xmax, ymin, ymax,
             depth=1):
    expr = 'z**2+c'
    for _ in xrange(depth-1):
        expr = '({expr})**2+c'.format(expr=expr)
    itermax = itermax/depth
    print 'Expression used:', expr
    ix, iy = mgrid[0:n, 0:m]
    x = linspace(xmin, xmax, n)[ix]
    y = linspace(ymin, ymax, m)[iy]
    c = x+complex(0,1)*y
    del x, y # save a bit of memory, we only need z
    img = zeros(c.shape, dtype=int)
    ix.shape = n*m
    iy.shape = n*m
    c.shape = n*m
    z = copy(c)
    for i in xrange(itermax):
        if not len(z): break # all points have escaped
        z = ne.evaluate(expr)
        rem = abs(z)>2.0
        img[ix[rem], iy[rem]] = i+1
        rem = -rem
        z = z[rem]
        ix, iy = ix[rem], iy[rem]
        c = c[rem]
    img[img==0] = itermax+1
    return img
 
if __name__=='__main__':
    from pylab import *
    import time
    doplot = True
    args = (1000, 1000, 100, -2, .5, -1.25, 1.25)
    start = time.time()
    I = mandel(*args)
    print 'Mandel time taken:', time.time()-start
    start = time.time()
    I2 = nemandel(*args)
    print 'Nemandel time taken:', time.time()-start
    start = time.time()
    I3 = nemandel(*args, depth=2)
    print 'Nemandel 2 time taken:', time.time()-start
    start = time.time()
    I4 = nemandel(*args, depth=3)
    print 'Nemandel 3 time taken:', time.time()-start
    for d in xrange(4, 9):
        start = time.time()
        I4 = nemandel(*args, depth=d)
        print 'Nemandel', d, 'time taken:', time.time()-start
 
    if doplot:
        subplot(221)
        img = imshow(I.T, origin='lower left')
        subplot(222)
        img = imshow(I2.T, origin='lower left')
        subplot(223)
        img = imshow(I3.T, origin='lower left')
        subplot(224)
        img = imshow(I4.T, origin='lower left')
        show()
