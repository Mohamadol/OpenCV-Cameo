import cv2
import numpy
import scipy.interpolate

def createCurveFunction(points):
    '''input 'points' is an array of pair of coordinates such as (x,y)
       '''
    
    if points is None:
        return None
    numberOfPoints = len(points)
    if numberOfPoints < 2:
        return None
    #get itterator through the coordinates
    xs, ys = zip(*points)
    if numberOfPoints < 4:
        kind = 'linear'
    else:
        kind = 'cubic'
    return scipy.interpolate.interp1d(x=xs, y=ys, kind=kind, bounds_error=False)


def createLookupArray(f, lenght=256):
    '''Creates a lookup array using function f passed as an arguement
       lenght indicates the size of channel (256 for 8 bits)'''
    if f is None:
        return
    #create an empty array with size = lenght
    lookupArray = numpy.empty(lenght)
    #start with index 0
    x = 0
    while x < lenght:
        #get the f(x) and bound between (0, lenght)
        lookupArray[x] = min(max(0,f(x)), lenght)
        x += 1
    return lookupArray


def searchLookupTable(lookupArray, src, dst):

    if lookupArray is None:
        return
    #create a new view to the looked up data in the destination array 
    dst[:] = lookupArray[src]


def createCompositeFunctions(f1, f2):
    '''returns the f1(f2(x)) composite function'''
    if f1 is None or f2 is None:
        return
    return lambda x: f1(f2(x))

def createFlatView(array):
    '''This fuction is useful for when the same function needs to be applied to
       all the channels a pixel have. It takes a possibly multi-dimensional array
       and returns a flatview interface to it (not a copy, just a reference to the
       same data) so that we can prevent split and merge of channels'''
    flatView = array.view()
    flatView.shape = array.size()
    return flatView


def isGrayScale(image):
    return image.ndim < 3

def getImageWidthHeight(image, divisor=1):
    w, h = image.shape[:2]
    return (w/divisor, h/divisor)






