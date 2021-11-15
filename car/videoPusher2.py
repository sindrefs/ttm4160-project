import threading
import picamera
import picamera.array
import requests
import cv2
import time
import json
import base64

running = True

# Image stream processing thread


class StreamProcessor(threading.Thread):
    def __init__(self):
        super(StreamProcessor, self).__init__()
        self.stream = picamera.array.PiRGBArray(camera)
        self.event = threading.Event()
        self.terminated = False
        self.start()
        self.begin = 0

    def run(self):
        global lastFrame
        global lockFrame
        # This method runs in a separate thread
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    # Read the image and save globally
                    self.stream.seek(0)
                    if flippedCamera:
                        flippedArray = cv2.flip(
                            self.stream.array, -1)  # Flips X and Y
                        retval, thisFrame = cv2.imencode(
                            '.jpg', flippedArray, [cv2.IMWRITE_JPEG_QUALITY, jpegQuality])
                        jpg_as_text = base64.b64encode(thisFrame)
                        requests.post("http://ttm41-bfflo-17c606og763lz-1083556350.eu-west-1.elb.amazonaws.com/image/", headers={"content-type": "application/json"},
                                      data=json.dumps({"image": str(jpg_as_text)[:-1]}))
                        del flippedArray
                    else:
                        retval, thisFrame = cv2.imencode('.jpg', self.stream.array, [
                            cv2.IMWRITE_JPEG_QUALITY, jpegQuality])
                    lockFrame.acquire()
                    lastFrame = thisFrame
                    lockFrame.release()
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()

# Image capture thread


class ImageCapture(threading.Thread):
    def __init__(self):
        super(ImageCapture, self).__init__()
        self.start()

    def run(self):
        global camera
        global processor
        print 'Start the stream using the video port'
        camera.capture_sequence(self.TriggerStream(),
                                format='bgr', use_video_port=True)
        print 'Terminating camera processing...'
        processor.terminated = True
        processor.join()
        print 'Processing terminated.'

    # Stream delegation loop
    def TriggerStream(self):
        global running
        while running:
            if processor.event.is_set():
                time.sleep(0.01)
            else:
                yield processor.stream
                processor.event.set()


# Create the image buffer frame
lastFrame = None
lockFrame = threading.Lock()


global camera
global imageWidth
global imageHeight
global frameRate

imageWidth = 240                        # Width of the captured image in pixels
imageHeight = 192                       # Height of the captured image in pixels
frameRate = 10  # Number of images to capture per second
displayRate = 10                        # Number of images to request per second
photoDirectory = '/home/pi'             # Directory to save photos to
# Swap between True and False if the camera image is rotated by 180
flippedCamera = True
jpegQuality = 80

print 'Setup camera'
camera = picamera.PiCamera()
camera.resolution = (imageWidth, imageHeight)
camera.framerate = frameRate


print 'Setup the stream processing thread'
processor = StreamProcessor()

print 'Wait ...'
time.sleep(2)
captureThread = ImageCapture()
