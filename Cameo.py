import cv2
from managers import WindowManager, CaptureManager
import filters
from trackers import FaceTracker
import rects

class Cameo:

    SPACE = 32
    TAB = 9
    ESCAPE = 27
    X = 120

    def __init__(self):
        self._windowManager = WindowManager('Cameo', self.onKeyPressed)
        self._captureManager = CaptureManager(capture=cv2.VideoCapture(0), previewWindowManager=self._windowManager, mirrorPreview=True)  
        self._curveFilter = filters.BGRPortraCurveFilter()
        self._faceTracker = FaceTracker()
        self._showDetectionRects = False
     
    def run(self):
        self._windowManager.createWindow()
        while self._windowManager.windowExists:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            self._faceTracker.update(frame)
            #self._curveFilter.apply(frame, frame)
            if self._showDetectionRects: 
                self._faceTracker.displayDetections(frame)
            self._captureManager.exitFrame()
            self._windowManager.processEvent()
            

    def onKeyPressed(self, keyCode):
        if keyCode == Cameo.SPACE:
            self._captureManager.writeImage('CameoScreenshot.png')
        elif keyCode == Cameo.TAB:
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo('CameoScreencast.avi')
            else:
                self._captureManager.stopWritingVideo()
        elif keyCode == Cameo.ESCAPE:
            self._windowManager.destroyWindow()
        elif keyCode == Cameo.X:
            self._showDetectionRects = not self._showDetectionRects 


cameo = Cameo()
cameo.run()