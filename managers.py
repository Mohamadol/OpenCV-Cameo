import cv2
import time
import numpy


class CaptureManager:

    def __init__(self, capture, previewWindowManager=None, mirrorPreview=False):

        self.previewWindowManager = previewWindowManager
        self.mirrorPreview = mirrorPreview

        self._capture = capture #instance of cv2.VideoCapture
        self._channel = 0   #cmera hardware to use
        self._frame = None  #image frame
        self._enteredFrame = False  #boolean returned by cv2.VideoCapture.grac()
        self._imageFileName = None  #file name used to save the image
        self._videoFileName = None  #file name to save the video
        self._videoEncoding = None  #codec used to save the video
        self._videoWriter = None    #instance of VideoWriter
        #variables below will be used to calculate the approximate FPS
        self._startTime = None  
        self._framesElapsed = 0
        self._fpsEstimate = None

    @property
    def channel(self):
        return self._channel

    @channel.setter 
    def channel(self, value):
        if self._channel != value:
            self._channel = value
            self._frame = None

    @property
    def frame(self):
        '''Retrieves the frame priviously grabed by enterFrame() method'''
        #if enteredFrame is True (grab() returned true, cameras are sync) 
        #and frame is None
        if self._enteredFrame and self._frame is None:
            #decodes and returns the grabbed video frame (returns ture/false,image)
            _, self._frame = self._capture.retrieve()
        return self._frame
 
    @property
    def isWritingImage(self):
        return self._imageFileName is not None

    @property
    def isWritingVideo(self):
        return self._videoFileName is not None

    def enterFrame(self):
        #check that exitFrame was called last time
        assert not self._enteredFrame
        if self._capture is not None:
            self._enteredFrame = self._capture.grab()

    def exitFrame(self):
        
        #retrieve the frame 
        if self.frame is None:
            self._enteredFrame = False
            return 
        #if no frame has been processed before, start the timer
        if self._framesElapsed == 0:
            self._startTime = time.time()
        else:
            #calculate estimated fps
            self._fpsEstimate = self._framesElapsed / (time.time() - self._startTime)
        self._framesElapsed += 1
        #if priview is enabled
        if self.previewWindowManager is not None:
            #if mirror over vertical axis is enabled
            if self.mirrorPreview:
                mirroredFrame = numpy.fliplr(self._frame).copy()
                self.previewWindowManager.showInWindow(mirroredFrame)
            else:
                self.previewWindowManager.showInWindow(self._frame)
        #if frame is to be saved in file directory
        if self.isWritingImage:
            cv2.imwrite(self._imageFileName, self._frame)
            self._imageFileName = None
        #call video writer
        self.writeVideoFrame()
        #prepare for next round 
        self._frame = None
        self._enteredFrame = False

    def writeImage(self, filename):
        self._imageFileName = filename
    
    def startWritingVideo(self, filename, encoding=cv2.VideoWriter_fourcc('I','4','2','0')):
        self._videoFileName = filename
        self._videoEncoding = encoding
    
    def stopWritingVideo(self):
        self._videoEncoding = None
        self._videoFileName = None
        self._videoWriter = None

    def writeVideoFrame(self):
        if not self.isWritingVideo:
            return
        
        if self._videoWriter is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            if fps == 0.0:
                if self._framesElapsed < 20:
                    return
                else:
                    fps = self._fpsEstimate
            size = (int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)),int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self._videoWriter = cv2.VideoWriter(self._videoFileName, self._videoEncoding, fps, size)
        self._videoWriter.write(self._frame)


class WindowManager:

    '''Provides an interface to create and distroy a named window, 
       display image frames in it and handle it\'s keypressed events'''

    def __init__(self, windowName, keyPressHandler=None):
        self.keyPressedHandler = keyPressHandler
        self._windowName = windowName
        self._windowExists = False
    
    @property
    def windowExists(self):
        return self._windowExists
    @windowExists.setter
    def windowExists(self, value):
        self._windowExists = value

    def createWindow(self):
        cv2.namedWindow(self._windowName)
        self.windowExists = True
    
    def showInWindow(self, frame):
        cv2.imshow(self._windowName, frame)

    def destroyWindow(self):
        cv2.destroyWindow(self._windowName)
        self.windowExists = False
    
    def processEvent(self):
        keycode = cv2.waitKey(1)
        if self.keyPressedHandler is not None and keycode != -1:
            keycode &= 0xFF
            self.keyPressedHandler(keycode)
    

     

    

    
    



    

