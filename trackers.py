import cv2
import rects
import utils

class Face:
    '''Holds data for a face (left & right eyes, nose and mouth)'''
    def __init__(self):
        self.faceRect = None
        self.LeftEyeRect = None
        self.RightEyeRect = None
        self.noseRect = None
        self.mouthRect = None


class FaceTracker:
    def __init__(self, scaleFactor=1.2, minNeighbors=2, flags=cv2.CASCADE_SCALE_IMAGE):
        self.scaleFactor = scaleFactor
        self.minNeighbors = minNeighbors
        self.flags = flags
        #a list to hold the most recent detected faces
        self._faces = []
        self._faceDetector = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt.xml')
        self._noseDetector = cv2.CascadeClassifier('cascades/haarcascade_mcs_nose.xml')
        self._eyeDetector = cv2.CascadeClassifier('cascades/haarcascade_eye.xml')
        self._mouthDetector = cv2.CascadeClassifier('cascades/haarcascade_mcs_mouth.xml')
    
    @property
    def face(self):
        return self._faces
    
    def update(self, image):
        #to reset the list for the new frame
        self._faces = []

        if not utils.isGrayScale(image):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY, image)
        image = cv2.equalizeHist(image)
        minSize = utils.getImageWidthHeight(image, 8)
        faceRects = self._faceDetector.detectMultiScale(image, self.scaleFactor, self.minNeighbors, self.flags, minSize)

        if faceRects is not None:
            for faceRect in faceRects:
                #create an object of type Face
                face = Face()
                #set the faceRect of face object to this faceRect
                face.faceRect = faceRect
                #get the coordinates from this faceRect
                x, y, w, h = faceRect
                #search for left eye in the upper left of the face
                searchRect = (x+w//7, y, w*2//7, h//2)
                face.LeftEyeRect = self._detectSubComponents(self._eyeDetector, image, searchRect, 64)
                #search for right eye in the upper left of the face
                searchRect = (x+w*4//7, y, w*2//7, h//2)
                face.RightEyeRect = self._detectSubComponents(self._eyeDetector, image, searchRect, 64)
                #search for the nose where it usually is in the face!
                searchRect = (x+w//4, y+h//2, w//2, h//2)
                face.noseRect = self._detectSubComponents(self._noseDetector, image, searchRect, 64)
                #search for the mouth where it usually is in the face!
                searchRect = (x+w//6, y+h*2//3, w*2//3, h//3)
                face.mouthRect = self._detectSubComponents(self._mouthDetector, image, searchRect, 64)
                self._faces.append(face)

    def _detectSubComponents(self, classifier, image, rect, imageToMinSizeRatio):
        minSize = utils.getImageWidthHeight(image, imageToMinSizeRatio)
        x, y, w, h = rect
        subImage = image[y:y+h, x:x+w]
        subComponentRects = classifier.detectMultiScale(subImage, self.scaleFactor, self.minNeighbors, self.flags, minSize)
        if len(subComponentRects) != 0:
            subx, suby, subw, subh = subComponentRects[0]
            #return the coordinates according to the original image
            return (x+subx, y+suby, subw, subh)
        else:
            return None

    
    def displayDetections(self, image):
        if utils.isGrayScale(image):
            faceFrameColor = 255
        else:
            faceFrameColor = (255,255,255)
            eyeFrameColor = (220,0,40)
            noseFrameColor = (0,255,0)
            mouthFrameColor = (10,10,10)
        for face in self._faces:
            rects.outlineRectangle((self._faces[len(self._faces)-1]).faceRect, image, faceFrameColor)
            rects.outlineRectangle((self._faces[len(self._faces)-1]).LeftEyeRect, image, eyeFrameColor)
            rects.outlineRectangle((self._faces[len(self._faces)-1]).RightEyeRect, image, eyeFrameColor)
            rects.outlineRectangle((self._faces[len(self._faces)-1]).noseRect, image, noseFrameColor)
            rects.outlineRectangle((self._faces[len(self._faces)-1]).mouthRect, image, mouthFrameColor)

