import cv2
import numpy
import utils


def strokeEdges(src, dest, blurKsize=7, edgeKsize=5):
    if blurKsize >= 3:
        blurredImage = cv2.medianBlur(src, blurKsize)
        grayImage = cv2.cvtColor(blurredImage, cv2.COLOR_BGR2GRAY)
    else:
        grayImage = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    cv2.Laplacian(grayImage, cv2.CV_8U, grayImage, edgeKsize)
    normalizedInverseAlpha = (255 - grayImage) / 255
    channels = cv2.split(src)
    for channel in channels:
        channel [:] = channel * normalizedInverseAlpha
    cv2.merge(channels, dest)


def RCChannelMixer(src, dest):
    ''' This function trasnfers the source image color channels from BGR
        to RC (Red, Cyan) channel by taking the average of Blue and Green
        channels and effectively mixing them. Pseudo Code looks like below:
        src.blue = src.green = (src.blue+src.green)/2
        src.red = src.red '''
    
    b, g, r = cv2.split(src)
    #args -> channel_1, weight, channel_2, weight, constant, destination_channel 
    cv2.addWeighted(b, 0.5, g, 0.5, 0, b)
    cv2.merge((b,b,r), dest)

def RGVChannelMixer(src, dest):
    '''This function trasnfers the source image color channels from BGR
        to RGV (Red, Green, Value) channel by setting all the blue pixels
        to the minimum of red or green or blue value of that pixel. 
        Pseudo Code looks like below:
        src.blue = min(src.blue, src.red, src.green)
        src.red = src.red 
        src.green = src.green '''
    
    b, g, r = cv2.split(src)
    cv2.min(b, g, b)
    cv2.min(b, r, b)
    cv2.merge((b,g,r), dest)

def CMVChannelMixer(src, dest):
    '''This function trasnfers the source image color channels from BGR
        to CMV (Cyan, Magneta, Value) channel by setting all the blue pixels
        to the maximum of red or green or blue value of that pixel. 
        Pseudo Code looks like below:
        src.blue = max(src.blue, src.red, src.green)
        src.red = src.red 
        src.green = src.green '''

    b, g, r = cv2.split(src)
    cv2.max(b, g, b)
    cv2.max(b, r, b)
    cv2.merge((b,g,r), dest)

#Classes to use when we only have a single channel or treat all the channels the same way
class VFuncFilter:
    '''Filter that applies a function to all the channels - V (value) or all the BGR'''
    def __init__(self, function=None, dataType=numpy.uint8):
        lenght = numpy.iinfo(dataType).max + 1
        self._lookupArray = utils.createLookupArray(function, lenght)

    def apply(self, src, dest):
        flatSrc = utils.createFlatView(src)
        flatDest = utils.createFlatView(dest)
        utils.searchLookupTable(self._lookupArray, flatSrc, flatDest)

class VCurveFilter(VFuncFilter):
    '''Interpolates a function from the given data and apply it'''
    def __init__(self, points, dataType = numpy.uint8):
        VFuncFilter.__init__(self, utils.createCurveFunction(points), dataType)

#Classes to use when we are dealing with multiple channels
class BGRFuncFilter:
    def __init__(self, vFunction=None, bFunction=None, gFunction=None, rFunction=None, dataType=numpy.uint8):
        lenght = numpy.iinfo(dataType).max + 1
        self._bLookupArray = utils.createLookupArray(utils.createCompositeFunctions(bFunction, vFunction), lenght)
        self._gLookupArray = utils.createLookupArray(utils.createCompositeFunctions(gFunction, vFunction), lenght)
        self._rLookupArray = utils.createLookupArray(utils.createCompositeFunctions(rFunction, vFunction), lenght)
    
    def apply(self, src, dest):
        b, g, r = cv2.split(src)
        utils.searchLookupTable(self._bLookupArray, b, b)
        utils.searchLookupTable(self._bLookupArray, g, g)
        utils.searchLookupTable(self._bLookupArray, r, r)
        dest = cv2.merge([b, g, r], dest)

class BGRCurveFilter(BGRFuncFilter):
    '''Interpolates a function from the given data and apply it'''
    def __init__(self, vPoints=None, bPoints=None, gPoints=None, rPoints=None, dataType = numpy.uint8):
        BGRFuncFilter.__init__(   \
            self,   \
            utils.createCurveFunction(vPoints), \
            utils.createCurveFunction(bPoints), \
            utils.createCurveFunction(gPoints), \
            utils.createCurveFunction(rPoints), \
            dataType)


class BGRPortraCurveFilter(BGRCurveFilter):
    '''This class hardcores control points to get a portra-like
       filter from BGRCurveFilter'''
    def __init__(self, dataType=numpy.uint8):
        BGRCurveFilter.__init__(    \
            self,   \
            vPoints = [(0,0),(23,20),(157,173),(255,255)],  \
            bPoints = [(0,0),(41,100),(231,228),(255,255)],  \
            gPoints = [(0,0),(52,47),(189,196),(255,255)],  \
            rPoints = [(0,0),(69,69),(213,218),(255,255)],  \
            dataType = dataType )
 

class BGRProviaCurveFilter(BGRCurveFilter):
    '''This class hardcores control points to get a provia-like
       filter from BGRCurveFilter'''
    def __init__(self, dataType=numpy.uint8):
        BGRCurveFilter.__init__(    \
            self,   \
            bPoints = [(0,0),(27,21),(196,207),(255,255)],  \
            gPoints = [(0,0),(52,47),(189,196),(255,255)],  \
            rPoints = [(0,0),(59,54),(202,210),(255,255)],  \
            dataType = dataType )


    

    

