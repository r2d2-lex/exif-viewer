from exif import Image
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from collections import namedtuple
import design
import os
import sys


class MyWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnOpen.clicked.connect(self.browse_folder)
        self.btnExit.clicked.connect(self.exit_program)
        self.btnDelete.clicked.connect(self.delete_exif_data)
        self.listFiles.itemClicked.connect(self.selection_changed)

        self.image_folder = ''
        self.support_extensions = '.jpg', '.jpeg'
        self.list_exif_files = []
        self.exif_tags = (
            ('lens_make', 'Lens make'),
            ('lens_model', 'Lens model'),
            ('lens_specification', 'Lens specification'),
            ('software', 'OS version'),
            ('gps_latitude', 'gps_latitude'),
            ('gps_latitude_ref', 'gps_latitude_ref'),
            ('gps_longitude', 'gps_longitude'),
            ('gps_longitude_ref', 'gps_longitude_ref'),
            ('datetime_original', 'datetime_original'),
            ('subsec_time_original', 'subsec_time_original'),
            ('offset_time', 'offset_time'),
        )

    def browse_folder(self):
        path = '.'
        self.listFiles.clear()
        self.image_folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выбрать папку', path)
        # self.listFiles.addItems(os.listdir(self.image_folder))
        for filename in os.listdir(self.image_folder):
            if filename.lower().endswith(self.support_extensions):
                self.listFiles.addItem(filename)

    def selection_changed(self, item):
        self.listAttrs.clear()
        print("Вы кликнули: {}".format(item.text()))
        image_full_path = '{}/{}'.format(self.image_folder,item.text())
        if self.chkPreview.isChecked():
            self.show_image(image_full_path)
        self.show_exif_info(image_full_path)

    def show_exif_info(self, image_path):
        with open(image_path, 'rb') as image_file:
            image_exif = Image(image_file)
            if image_exif.has_exif:
                status = f"contains EXIF (version {image_exif.exif_version}) information."
                self.show_exif_tags_info(image_exif)
            else:
                status = "does not contain any EXIF information."
            print(f"Image {status}")

    def show_exif_tags_info(self, image_exif):
        print(dir(image_exif))
        EXIF_TAGS = namedtuple('EXIF_TAGS', 'tag description')
        for _record in self.exif_tags:
            record = EXIF_TAGS(*_record)
            tag = image_exif.get(record.tag, 'Unknown')
            self.listAttrs.addItem(f'{record.description}: {tag}')
        # self.listAttrs.addItem(f'{image_exif.datetime_original}.{image_exif.subsec_time_original}')
        # self.listAttrs.addItem(f'Latitude: {image_exif.gps_latitude} {image_exif.gps_latitude_ref}')
        # self.listAttrs.addItem(f'Longitude: {image_exif.gps_longitude} {image_exif.gps_longitude_ref}')

    def delete_exif_data(self, image_exif):
        image_exif.delete_all()

    def delete_exif_tag(self, image_exif, tag):
        image_exif.delete(tag)

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

    @staticmethod
    def exit_program():
        QApplication.quit()


def main():
    app = QtWidgets.QApplication([])
    application = MyWindow()
    application.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
