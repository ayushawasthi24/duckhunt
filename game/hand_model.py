import mediapipe as mp
import cv2
import time
import pylab as pl
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

class HandGestureModel:
    """
    A class that represents a hand gesture recognition model.

    Args:
        model_path (str): The path to the gesture recognition model file.
        dim (tuple): The dimensions (width, height) of the video frame.

    Attributes:
        recognizer (GestureRecognizer): The gesture recognizer object.
        vid (cv2.VideoCapture): The video capture object for accessing the webcam.
        mouse_pos (tuple): The current position of the mouse (x, y).
        result (GestureRecognizerResult): The result of the gesture recognition.

    Methods:
        callback: A callback function called when a gesture is recognized.
        get_pos: Get the current position of the mouse based on hand landmarks.
        is_click: Check if a thumb-up gesture is detected (indicating a click).

    """
    def __init__(self, model_path: str = './outfile.task', dim: tuple = (0, 0)):
        """
        Initializes the HandGestureModel object.

        Args:
            model_path (str): The path to the gesture recognition model file.
            dim (tuple): The dimensions (width, height) of the video frame.
        """
        options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self.callback)#setting options for inference
        self.recognizer = GestureRecognizer.create_from_options(options)#Hand Gesture Model
        self.dim = dim
        self.vid = cv2.VideoCapture(0)#webcam
        self.mouse_pos = (1, 1)
        self.result = GestureRecognizerResult([], [], [], [])
        self.clicked=False

    def callback(self, result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        """
        A callback function called when a gesture is recognized.

        Args:
            result (GestureRecognizerResult): The result of the gesture recognition.
            output_image (mp.Image): The processed image with landmarks and annotations.
            timestamp_ms (int): The timestamp of the image in milliseconds.
        """
        if len(result.hand_landmarks) > 0:
            self.result = result
            res = result.hand_landmarks[0][8]
            self.mouse_pos = ((1 - res.x) * self.dim[0], res.y * self.dim[1])

    def get_pos(self):
        """
        Get the current position of the mouse based on hand landmarks.

        Returns:
            tuple: The current position of the mouse (x, y).
        """
        ret, frame = self.vid.read()
        try: mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        except: return self.mouse_pos
        self.recognizer.recognize_async(mp_image, int(time.time() * 1000))
        return self.mouse_pos
    def is_click(self):
        """
        Check if a thumb-up gesture is detected (indicating a click).

        Returns:
            bool: True if a thumb-up gesture is detected, False otherwise.
        """
        if(len(self.result.gestures) > 0):
            print(self.result.gestures[0][0].category_name)
            if(self.clicked):
                if(self.result.gestures[0][0].category_name != "Pointing_Up"):
                    self.clicked = False
                else:
                    self.clicked = True
                return False
            else:
                if(self.result.gestures[0][0].category_name == "Pointing_Up"):
                    self.clicked = True
                    return True
                else:return False