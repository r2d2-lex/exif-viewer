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
        self.btnDelete.clicked.connect(self.delete_exif_info)
        self.listFiles.itemClicked.connect(self.selection_changed)
        self.btnSave.clicked.connect(self.print_status)
        # self.listFiles.itemPressed.connect(self.multi_selection_changed)

        self.image_folder = ''
        self.support_extensions = '.jpg', '.jpeg'
        self.list_exif_files = []

    def browse_folder(self):
        path = '.'
        self.listFiles.clear()
        self.image_folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выбрать папку', path)
        # self.listFiles.addItems(os.listdir(self.image_folder))
        for filename in os.listdir(self.image_folder):
            if filename.lower().endswith(self.support_extensions):
                self.listFiles.addItem(filename)

    def multi_selection_changed(self):
        items = self.listFiles.selectedItems()
        self.list_exif_files = []
        for i in range(len(items)):
            self.list_exif_files.append(str(self.listFiles.selectedItems()[i].text()))
        self.print_status(f'ВЫбранные файлы: {self.list_exif_files}')

    def selection_changed(self, item):
        self.multi_selection_changed()
        if len(self.list_exif_files) <= 1:
            file_name = item.text()
            if not self.list_exif_files:
                self.list_exif_files.append(file_name)

            self.listAttrs.clear()
            self.print_status(f'Вы кликнули: {file_name}')
            image_full_path = self.get_full_path(file_name)
            if self.chkPreview.isChecked():
                self.show_image(image_full_path)

            with ExifImage(image_full_path) as exif_file:
                print(exif_file.show_exif_info())
                tags_info_records = exif_file.show_exif_tags_info()
                print(tags_info_records)
                for record in tags_info_records:
                    self.listAttrs.addItem(record)
        print('\r\n')

    def show_image(self, image_path):
        print(f'Show image path: {image_path}')
        pix = QPixmap(image_path)

        # Scale image
        # self.graphView.resize(pix.width(), pix.height())
        height, width = self.graphView.height(), self.graphView.width()
        pix = pix.scaled(height - 10, width - 10)

        item = QtWidgets.QGraphicsPixmapItem(pix)
        scene = QtWidgets.QGraphicsScene(self)
        scene.addItem(item)
        self.graphView.setScene(scene)

    def delete_exif_info(self):
        if self.list_exif_files:
            for filename in self.list_exif_files:
                print(f'Delete info for {filename}')
                with ExifImage(self.get_full_path(filename)) as exif_file:
                    if self.chkAlterName.isChecked():
                        exif_file.delete_exif_data(new_name=True)
                    else:
                        exif_file.delete_exif_data()

    def get_full_path(self, file_name=''):
        return os.path.join(self.image_folder, file_name)

    def print_status(self, message=' '):
        self.statusbar.showMessage(message)
        print(message)

    @staticmethod
    def exit_program():
        QApplication.quit()


class ExifImage:
    def __init__(self, name: str):
        self.name = name
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

    def __enter__(self):
        self.image_file = open(self.name, 'rb+')
        if self.image_file:
            self.image_exif = Image(self.image_file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.image_file:
            self.image_file.close()

    def show_exif_info(self):
        status = False
        if self.image_exif.has_exif:
            message = f"contains EXIF (version {self.image_exif.exif_version}) information."
            status = self.image_exif.exif_version
        else:
            message = "does not contain any EXIF information."
        print(f"Image {message}")
        return status

    def delete_exif_data(self, new_name=False):
        if self.image_exif.has_exif:
            self.image_exif.delete_all()
            if new_name:
                self.write_with_new_name()
            else:
                self.write_image_exif()

    def delete_exif_tag(self, tag: str, new_name=False):
        if self.image_exif.has_exif:
            self.image_exif.delete(tag)
            if new_name:
                self.write_with_new_name()
            else:
                self.write_image_exif()

    def write_with_new_name(self):
        with open(f'{self.name}_mdf', 'wb') as image_file:
            image_file.write(self.image_exif.get_file())

    def write_image_exif(self):
        self.image_file.seek(0)
        self.image_file.write(self.image_exif.get_file())

    def show_exif_tags_info(self) -> list:
        attrs_list = []
        if self.image_exif.has_exif:
            EXIF_TAGS = namedtuple('EXIF_TAGS', 'tag description')
            for _record in self.exif_tags:
                record = EXIF_TAGS(*_record)
                tag = self.image_exif.get(record.tag, 'Unknown')
                attrs_list.append(f'{record.description}: {tag}')
        return attrs_list


def main():
    app = QtWidgets.QApplication([])
    application = MyWindow()
    application.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
