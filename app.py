from exif import Image
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import design
import os
import sys


class MyWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnOpen.clicked.connect(self.browse_folder)
        self.listFiles.itemClicked.connect(self.selection_changed)

        self.image_folder = ''
        self.support_extensions = '.jpg', '.jpeg'

    def browse_folder(self):
        path = '.'
        self.listFiles.clear()
        self.image_folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выбрать папку', path)
        # self.listFiles.addItems(os.listdir(self.image_folder))
        for filename in os.listdir(self.image_folder):
            if filename.lower().endswith(self.support_extensions):
                self.listFiles.addItem(filename)

    def selection_changed(self, item):
        print("Вы кликнули: {}".format(item.text()))
        image_full_path = '{}/{}'.format(self.image_folder,item.text())
        self.show_image(image_full_path)
        self.show_exif_info(image_full_path)

    def show_exif_info(self, image_path):
        with open(image_path, 'rb') as image_file:
            image_exif = Image(image_file)
            if image_exif.has_exif:
                status = f"contains EXIF (version {image_exif.exif_version}) information."
            else:
                status = "does not contain any EXIF information."
            print(f"Image {status}")

    def show_image(self, image_path):
        pix = QPixmap(image_path)

        # Scale image
        # self.graphView.resize(pix.width(), pix.height())
        height, width = self.graphView.height(), self.graphView.width()
        pix = pix.scaled(height-10, width-10)

        item = QtWidgets.QGraphicsPixmapItem(pix)
        scene = QtWidgets.QGraphicsScene(self)
        scene.addItem(item)
        self.graphView.setScene(scene)


def main():
    app = QtWidgets.QApplication([])
    application = MyWindow()
    application.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
