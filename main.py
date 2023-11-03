# coding:utf-8
import sys
import PyQt5
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog
from PyQt5.QtCore import pyqtSlot
from qfluentwidgets import PushButton, LineEdit, setTheme, Theme, SubtitleLabel, CaptionLabel, FlyoutView, Flyout, InfoBarIcon
import webbrowser
from urllib import parse
import zipfile
import shutil
import subprocess
import os

print("loading please wait...")


class ConvertWindow(QWidget):
    def __init__(self):
        # This will create the full UI in the ConvertWindow Widget
        super().__init__()
        self.resize(500, 250)
        self.setWindowTitle("Wallpaper Engine To Lively 1.4")
        # Dark Theme
        self.setStyleSheet("ConvertWindow {background: rgb(32, 32, 32)}")
        # Layout
        setTheme(Theme.DARK)
        self.app_title = SubtitleLabel("Wallpaper Engine Convertor", self)
        self.label_url = CaptionLabel("Workshop URL", self)
        self.input_url = LineEdit(self)
        self.workshop_button = PushButton("Open Workshop", self)
        self.download_button = PushButton("Download From Workshop", self)
        self.convert_button = PushButton("Convert Wallpaper", self)
        self.check_button = PushButton("Check Wallpaper Format", self)
        self.download_button.clicked.connect(self.download_file)
        self.workshop_button.clicked.connect(self.open_workshop)
        self.convert_button.clicked.connect(self.convert)
        self.check_button.clicked.connect(self.check)
        self.app_title.setContentsMargins(0, 0, 0, 15)

        # Layout of the app
        layout_hz = QVBoxLayout()
        layout_hz.addWidget(self.app_title)
        layout_hz.addWidget(self.label_url)
        layout_hz.addWidget(self.input_url)
        layout_hz.addWidget(CaptionLabel("Options", self))
        layout_hz.addWidget(self.workshop_button)
        layout_hz.addWidget(self.download_button)
        layout_hz.addWidget(self.check_button)
        layout_hz.addWidget(self.convert_button)
        self.setLayout(layout_hz)


    def download_file(self):
        # Open a webpage for the user to download the background
        try:
            url_workshop = parse.urlparse(self.input_url.text()).query
            id_workshop = parse.parse_qs(url_workshop)['id'][0]
            webbrowser.open("http://steamworkshop.download/download/view/" + str(id_workshop))
        # If the url does not contain the required ID for download
        except KeyError:
            Flyout.create(
                icon=InfoBarIcon.ERROR,
                title='Invalid URL',
                content="Your URL should contains a Steam workshop IDx",
                target=self.download_button,
                parent=self,
                isClosable=True
            )

    def convert(self):
        # Function to covert the zip file to usable background
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter('Zip Files (*.zip)')

        if file_dialog.exec_() == QFileDialog.Accepted:
            selected_file_path = file_dialog.selectedFiles()[0]

            with zipfile.ZipFile(selected_file_path, 'r') as zip_ref:  # Unzip the file to copy the video
                zip_ref.extractall()

            file_path = os.path.splitext(selected_file_path)[0]  # Get the folder name
            file_name = os.path.basename(file_path)
            if mp4_file := [files for files in os.listdir(file_name) if files.endswith('.mp4')]:
                # Convert the file if the format is .mp4
                shutil.copy(file_name + "\\" + mp4_file[0], os.curdir)  # Copy the video
                shutil.copy(file_name + "\\preview.jpg", os.curdir)  # Copy the preview
                shutil.rmtree(file_name)  # Delete the old folder
                cmd_to_open = rf'explorer /select,"{os.getcwd()}\{mp4_file[0]}"'

                done_flyout = FlyoutView(
                    icon=InfoBarIcon.SUCCESS,
                    title='Done',
                    parent=self,
                    content=f"{file_name}.zip was converted",
                    isClosable=True,
                    image='preview.jpg'
                )

                view_file_button = PushButton('View in File Explorer')
                view_file_button.clicked.connect((lambda: self.view_file(cmd_to_open)))
                done_flyout.addWidget(view_file_button, align=Qt.AlignLeft)

                w = Flyout.make(done_flyout, self.convert_button, self)
                done_flyout.closed.connect(w.close)

    def check(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter('Zip Files (*.zip)')

        if file_dialog.exec_() == QFileDialog.Accepted:
            selected_file_path = file_dialog.selectedFiles()[0]
            selected_file_zip = zipfile.ZipFile(selected_file_path)

            if [files for files in selected_file_zip.namelist() if files.endswith('.mp4')]:
                Flyout.create(
                    icon=InfoBarIcon.SUCCESS,
                    title='Success',
                    content="Your wallpaper is in the .mp4, Can be converted",
                    target=self.check_button,
                    parent=self,
                    isClosable=True
                )
            else:
                Flyout.create(
                    icon=InfoBarIcon.WARNING,
                    title='Warning',
                    content="Your wallpaper is not in the .mp4, Could be extracted but not guaranteed (.PKG EXTRACTING SOON)",
                    target=self.check_button,
                    parent=self,
                    isClosable=True
                )

    def view_file(self, cmd):
        # Open the background in the file explorer, from the flyout button
        # CMD (str): The command to run EXAMPLE: 'explorer /select {PATH}'
        subprocess.Popen(cmd)


    def open_workshop(self):
        warning_workshop = FlyoutView(
            icon=InfoBarIcon.WARNING,
            title='Warning',
            content="Use popular wallpapers before 2022.\nOr will you get a \"Free Space Left\" error (meaning: the file is not found)",
            parent=self,
            isClosable=True
        )

        open_workshop_url = PushButton("Open Workshop")
        open_workshop_url.clicked.connect(self.open_workshop_url)
        warning_workshop.addWidget(open_workshop_url, align=Qt.AlignLeft)


        w = Flyout.make(warning_workshop, self.workshop_button, self)
        warning_workshop.closed.connect(w.close)


    def open_workshop_url(self):
        webbrowser.open("https://steamcommunity.com/workshop/browse/?appid=431960&searchtext=&childpublishedfileid=0&browsesort=trend&section=readytouseitems&requiredtags%5B%5D=Video&requiredtags%5B%5D=Everyone&created_date_range_filter_start=0&created_date_range_filter_end=0&updated_date_range_filter_start=0&updated_date_range_filter_end=0")

if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    w = ConvertWindow()
    w.show()
    app.exec_()
