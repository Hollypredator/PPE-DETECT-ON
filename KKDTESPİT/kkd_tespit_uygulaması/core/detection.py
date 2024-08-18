from roboflow import Roboflow
import numpy as np
import cv2

class KKDModel:
    def __init__(self, api_key, project_name, version):
        self.api_key = api_key
        self.project_name = project_name
        self.version = version
        self.rf = Roboflow(api_key=self.api_key)
        self.project = self.rf.workspace().project(self.project_name)
        self.model = self.project.version(self.version).model

    def detect(self, frame):
        # Convert frame to RGB and then to a numpy array
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_array = np.array(frame_rgb)

        # Perform prediction
        result = self.model.predict(img_array, confidence=40, overlap=30).json()
        return result

    def render_results(self, frame, result):
        # Example implementation of rendering results (detection boxes) on the frame
        for prediction in result['predictions']:
            x_min = int(prediction['x'] - prediction['width'] / 2)
            y_min = int(prediction['y'] - prediction['height'] / 2)
            x_max = int(prediction['x'] + prediction['width'] / 2)
            y_max = int(prediction['y'] + prediction['height'] / 2)
            label = prediction['class']
            confidence = prediction['confidence']

            # Draw bounding box
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
            cv2.putText(frame, f"{label} ({confidence:.2f})", (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        return frame
