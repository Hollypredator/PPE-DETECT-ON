import cv2
import numpy as np
import os
import datetime
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from core.detection import KKDModel
import config

class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_camera()
        self.init_model()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def init_ui(self):
        self.setWindowTitle("Kişisel Koruma Ekipmanları Tespit")
        self.setGeometry(100, 100, 800, 600)
        self.image_label = QLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

    def init_camera(self):
        self.cap = cv2.VideoCapture(config.CAMERA_INDEX)
        if not self.cap.isOpened():
            print("Kamera açılamadı!")
            sys.exit()

    def init_model(self):
        self.model = KKDModel(api_key=config.ROBOFLOW_API_KEY, project_name=config.PROJECT_NAME, version=config.PROJECT_VERSION)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Kamera görüntüsü okunamadı!")
            return

        result = self.model.detect(frame)
        frame = self.model.render_results(frame, result)

        if frame is not None and frame.size != 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channels = frame_rgb.shape
            bytes_per_line = channels * width
            q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.image_label.setPixmap(QPixmap.fromImage(q_image))

            # Kaydetme işlemi
            self.save_screenshot_if_needed(frame, result)
        else:
            print("Görüntü verisi mevcut değil!")

    def save_screenshot_if_needed(self, frame, result):
        save_dir = 'screenshots'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Kontrol et ve sadece belirtilen durumlar için ekran görüntüsü al
        for prediction in result['predictions']:
            label = prediction['class']
            if label in ['no helmet', 'no vest']:  # Örnek etiketler, ihtiyacınıza göre güncelleyin
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{label}_{timestamp}.jpg"
                file_path = os.path.join(save_dir, file_name)

                cv2.imwrite(file_path, frame)
                print(f"Ekran görüntüsü kaydedildi: {file_path}")
                break  # İlk tespitte ekran görüntüsünü alır ve döngüden çıkar
