from PyQt5.QtWidgets import QApplication
from gui.camera_widget import CameraWidget

def main():
    app = QApplication([])
    window = CameraWidget()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
