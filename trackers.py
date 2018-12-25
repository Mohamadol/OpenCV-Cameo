import cv2
import rects
import utils

class FacialTracker:

    def __init__(self):
        self.faceRect = None
        self.LeftEyeRect = None
        self.RightEyeRect = None
        self.noseRect = None
        self.mouthRect = None
        
