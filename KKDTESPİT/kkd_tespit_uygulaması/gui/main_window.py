from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget
from gui.camera_widget import CameraWidget
import os

class KKDApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("KKD Tespit Uygulaması")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Kamera görüntü widget'ını ekle
        self.camera_widget = CameraWidget(self)
        self.layout.addWidget(self.camera_widget)

        # Ekran görüntüsü alma düğmesi
        self.capture_button = QPushButton("İhlali Kaydet", self)
        self.capture_button.clicked.connect(self.save_screenshot)
        self.layout.addWidget(self.capture_button)

    def save_screenshot(self):
        image_path = os.path.join("data/screenshots/", "screenshot.png")
        self.camera_widget.save_screenshot(image_path)
        print(f"Görüntü kaydedildi: {image_path}")
