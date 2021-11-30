import cv2
import io
import time
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera

class PiCam:
    def __init__(self, show=True, framerate=25, width=640, height=480):
        self.size = (width, height)
        self.show = show
        self.framerate = framerate
        self.camera = PiCamera()
        self.camera.rotation = 180
        self.camera.resolution = self.size
        self.camera.framerate = self.framerate

    def snapshot(self):
        frame = io.BytesIO()
        self.camera.capture(frame, 'jpeg',use_video_port=True)
        frame.seek(0)
        return frame.getvalue()

    def __iter__(self):
        rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
        rawCapture.truncate(0)
        for frame in camera.capture_continuous(rawCapture, format="bgr",
                                                use_video_port=True):
            yield frame.array
            rawCapture.truncate(0)

    def run(self, callback=None):
        rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
        rawCapture.truncate(0)
        for frame in self.camera.capture_continuous(rawCapture, format="bgr",
                                                    use_video_port=True):
            image = frame.array
            if callback and not callback(image): break
            if(self.show or callback == None):
                cv2.imshow('frame', image)
                key = cv2.waitKey(1)
                if key == 27: break
            rawCapture.truncate(0)
        
        cv2.destroyAllWindows()

class MJpegStreamCam(PiCam):
    def __init__(self, show=True, framerate=25, width=640, height=480):
        super().__init__(show=show, framerate=framerate, width=width, height=height)

    def __iter__(self):
        frame = io.BytesIO()
        while True:
            self.camera.capture(frame, format="jpeg", use_video_port=True)
            frame.seek(0)
            image = frame.getvalue()
            yield (b'--myboundary\n'
                b'Content-Type:image/jpeg\n'
                b'Content-Length: ' + f"{len(image)}".encode() + b'\n'
                b'\n' + image + b'\n')
            frame.truncate()
            # time.sleep(1/self.framerate)