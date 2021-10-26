import os
import shutil
from functools import partial

import cv2 as cv
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMainWindow, QPushButton, QInputDialog, QFileDialog, QListWidget, QListWidgetItem
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from images_dialog import ImagesDialog
from calibrator import Calibrator


class MainWindow(QMainWindow):
    dir_path = os.getcwd()

    def __init__(self):
        super().__init__()
        self.thread_dict = {}

    def setup_ui(self):
        self.setWindowTitle("Калибровка камер")
        self.setFixedSize(720, 620)
        centralwidget = QtWidgets.QWidget(self, objectName="centralwidget")
        verticalLayoutWidget = QtWidgets.QWidget(centralwidget, objectName="verticalLayoutWidget")
        verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 210, 590))
        verticalLayout = QtWidgets.QVBoxLayout(verticalLayoutWidget)
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        horizontalLayout = QtWidgets.QHBoxLayout()

        pushButton = QPushButton(verticalLayoutWidget, text="Добавить камеру", objectName="create_cam")
        horizontalLayout.addWidget(pushButton)

        verticalLayout.addLayout(horizontalLayout)

        pushButton_2 = QPushButton(verticalLayoutWidget, text="Удалить камеру", objectName="delete_cam")
        horizontalLayout.addWidget(pushButton_2)

        list_widget = QListWidget(verticalLayoutWidget)
        list_widget.setObjectName("cam_list")
        verticalLayout.addWidget(list_widget)

        verticalLayoutWidget_2 = QtWidgets.QWidget(centralwidget)
        verticalLayoutWidget_2.setGeometry(QtCore.QRect(230, 10, 480, 591))
        verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")

        verticalLayout_2 = QtWidgets.QVBoxLayout(verticalLayoutWidget_2)
        verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        verticalLayout_2.setObjectName("verticalLayout_2")

        horizontalLayout_0 = QtWidgets.QHBoxLayout()
        verticalLayout_2.addLayout(horizontalLayout_0)

        checkBox = QtWidgets.QCheckBox(verticalLayoutWidget_2, text='Кадр в секунду', objectName='all')
        horizontalLayout_0.addWidget(checkBox)

        label = QtWidgets.QLabel(verticalLayoutWidget_2, text="Выберите камеру")
        label.setObjectName("cam_name")
        horizontalLayout_0.addWidget(label)


        horizontalLayout_6 = QtWidgets.QHBoxLayout()
        horizontalLayout_6.setObjectName("horizontalLayout_6")

        verticalLayout_4 = QtWidgets.QVBoxLayout()
        verticalLayout_4.setObjectName("verticalLayout_4")

        horizontalLayout_6.addLayout(verticalLayout_4)

        verticalLayout_4 = QtWidgets.QVBoxLayout()
        verticalLayout_4.setObjectName("verticalLayout_4")

        horizontalLayout_5 = QtWidgets.QHBoxLayout()
        horizontalLayout_5.setObjectName("horizontalLayout_5")

        pushButton_5 = QPushButton(verticalLayoutWidget_2, text="Добавить видео", objectName='add_video')
        horizontalLayout_5.addWidget(pushButton_5)

        pushButton_6 = QPushButton(verticalLayoutWidget_2, text="Удалить видео", objectName='delete_video')
        horizontalLayout_5.addWidget(pushButton_6)

        verticalLayout_4.addLayout(horizontalLayout_5)

        list_widget_3 = QListWidget(verticalLayoutWidget_2)
        list_widget_3.setObjectName("vid_list")
        verticalLayout_4.addWidget(list_widget_3)

        horizontalLayout_6.addLayout(verticalLayout_4)

        verticalLayout_7 = QtWidgets.QVBoxLayout()
        verticalLayout_7.setObjectName("verticalLayout_7")
        horizontalLayout_7 = QtWidgets.QHBoxLayout()
        horizontalLayout_7.setObjectName("horizontalLayout_7")

        pushButton_11 = QPushButton(verticalLayoutWidget_2, text="Добавить кадр", objectName='add_frame')
        horizontalLayout_7.addWidget(pushButton_11)

        pushButton_12 = QPushButton(verticalLayoutWidget_2, text="Удалить кадр", objectName='delete_frame')
        horizontalLayout_7.addWidget(pushButton_12)

        verticalLayout_7.addLayout(horizontalLayout_7)

        list_widget_4 = QListWidget(verticalLayoutWidget_2)
        list_widget_4.setObjectName("frames_list")

        verticalLayout_7.addWidget(list_widget_4)

        horizontalLayout_6.addLayout(verticalLayout_7)

        verticalLayout_6 = QtWidgets.QVBoxLayout()
        verticalLayout_6.setObjectName("verticalLayout_6")

        pushButton_8 = QPushButton(verticalLayoutWidget_2, text="Выбрать кадры", objectName='choose_frames')
        verticalLayout_6.addWidget(pushButton_8, alignment=QtCore.Qt.AlignTop)

        pushButton_7 = QPushButton(verticalLayoutWidget_2, text="Углы", objectName='corners')
        verticalLayout_6.addWidget(pushButton_7, alignment=QtCore.Qt.AlignBottom)

        pushButton_9 = QPushButton(verticalLayoutWidget_2, text="Убрать дисторции", objectName='undistortion')
        verticalLayout_6.addWidget(pushButton_9)

        pushButton_10 = QPushButton(verticalLayoutWidget_2, text="Без дисторций", objectName='show_undistortions')
        verticalLayout_6.addWidget(pushButton_10)

        horizontalLayout_6.addLayout(verticalLayout_6)
        verticalLayout_2.addLayout(horizontalLayout_6)

        progressBar = QtWidgets.QProgressBar(verticalLayoutWidget_2)
        progressBar.setObjectName("progressBar")
        verticalLayout_2.addWidget(progressBar)

        pushButton_10 = QPushButton(verticalLayoutWidget_2, text="Калибровка", objectName='calibration')
        verticalLayout_2.addWidget(pushButton_10)

        MainWindow.setCentralWidget(self, centralwidget)

        menubar = QtWidgets.QMenuBar(self)
        menubar.setGeometry(QtCore.QRect(0, 0, 872, 26))
        menubar.setObjectName("menubar")
        menu = QtWidgets.QMenu(menubar)
        menu.setObjectName("menu")
        menu.setTitle("Настройки")
        MainWindow.setMenuBar(self, menubar)

        statusbar = QtWidgets.QStatusBar(self)
        statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self, statusbar)

        QtCore.QMetaObject.connectSlotsByName(self)

    def set_logic(self):
        self.create_dir(self.dir_path, 'cameras')
        self.findChild(QPushButton, 'create_cam').clicked.connect(self.create_cam)
        self.findChild(QPushButton, 'delete_cam').clicked.connect(self.delete_cam)
        self.findChild(QPushButton, 'add_video').clicked.connect(self.add_video)
        self.findChild(QPushButton, 'delete_video').clicked.connect(self.delete_video)
        self.findChild(QPushButton, 'choose_frames').clicked.connect(self.add_video_frames)
        self.findChild(QPushButton, 'add_frame').clicked.connect(self.add_frame)
        self.findChild(QPushButton, 'delete_frame').clicked.connect(self.delete_frame)
        self.findChild(QPushButton, 'calibration').clicked.connect(self.calibrate_cam)
        self.findChild(QPushButton, 'corners').clicked.connect(self.show_corners)
        self.findChild(QPushButton, 'undistortion').clicked.connect(self.undistortion)
        self.findChild(QtWidgets.QCheckBox, 'all').setChecked(True)
        self.findChild(QPushButton, 'show_undistortions').clicked.connect(self.show_undistortions)
        list_widget = self.findChild(QListWidget, 'cam_list')
        list_widget.itemClicked.connect(self.set_cam_data)
        self.collect_data('\\cameras', "cam_list")

    def set_cam_data(self):
        list_widget = self.findChild(QListWidget, 'cam_list')
        item = list_widget.selectedItems()[0]
        if item:
            cam_name = item.text()
            label = self.findChild(QtWidgets.QLabel, 'cam_name')
            label.setText(cam_name)
            self.clear_list("vid_list")
            self.clear_list("frames_list")
            self.collect_data(f'\\cameras\\{cam_name}\\frames', "frames_list")
            self.collect_data(f'\\cameras\\{cam_name}\\videos', "vid_list")
            self.findChild(QPushButton, 'calibration').setEnabled(cam_name not in self.thread_dict.keys())
            self.findChild(QPushButton, 'undistortion').setEnabled(cam_name not in self.thread_dict.keys())
            self.findChild(QPushButton, 'add_video').setEnabled(cam_name not in self.thread_dict.keys())
            self.findChild(QtWidgets.QProgressBar, 'progressBar').setProperty("value", 0)

    def get_sel_cam(self):
        cam = self.findChild(QListWidget, 'cam_list').selectedItems()
        return cam[0] if cam else None

    def clear_list(self, list_name):
        list_widget = self.findChild(QListWidget, list_name)
        list_widget.clear()

    def create_dir(self, path, name):
        abs_path = path + '\\' + name
        if not os.path.exists(abs_path):
            os.mkdir(abs_path)

    def create_cam(self):
        dlg = QInputDialog()
        dlg.setWindowTitle('Добавление')
        dlg.setFixedSize(270, 120)
        dlg.setLabelText("Введите название камеры.")
        dlg.exec()
        cam_name = dlg.textValue()
        cam_list_widget = self.findChild(QListWidget, 'cam_list')
        cam_list_name = [cam_list_widget.item(x).text() for x in range(cam_list_widget.count())]

        if cam_name is not None and dlg.result():
            if cam_name not in cam_list_name and cam_name != '':
                item = QListWidgetItem(cam_name)
                cam_list_widget.addItem(item)

                self.create_dir(self.dir_path + '\\cameras', cam_name)
                self.create_dir(f'{self.dir_path}\\cameras\\{cam_name}', 'videos')
                self.create_dir(f'{self.dir_path}\\cameras\\{cam_name}', 'frames')
                self.create_dir(f'{self.dir_path}\\cameras\\{cam_name}', 'corners')
                self.create_dir(f'{self.dir_path}\\cameras\\{cam_name}', 'undistortions')

    def delete_cam(self):
        ########### Вы уверены, это удалит всю информацию о камере???
        cam_list = self.findChild(QListWidget, 'cam_list')
        cam = self.get_sel_cam()
        if cam is not None:
            cam_name = cam.text()
            if cam_name in self.thread_dict.keys():
                self.thread_dict[cam_name][0].qiut()
                self.thread_dict.pop(cam_name)
            cam_list.takeItem(cam_list.row(cam))
            path = self.dir_path + '\\cameras\\' + cam_name
            if os.path.exists(path):
                shutil.rmtree(path)
            label = self.findChild(QtWidgets.QLabel, 'cam_name')
            if label.text() == cam_name:
                self.clear_list("frames_list")
                label.setText('Выберите камеру')

    def add_video(self):
        list_widget = self.findChild(QListWidget, 'cam_list')
        cam = list_widget.selectedItems()
        if cam:
            cam_name = cam[0].text()
            path = QFileDialog.getOpenFileName(self, "Выберите видео", "",
                                               "Video Files (*.mp4 *.avi *.mkv *.mpg)")[0]
            if path:
                vid_name = path.split('/')[-1]
                vid_name = vid_name[:vid_name.rfind('.')]
                self.create_dir(f'{self.dir_path}\\cameras\\{cam_name}\\videos', vid_name)

                per_sec = self.findChild(QtWidgets.QCheckBox, 'all').isChecked()

                self.extract(path, per_sec, vid_name)

    def delete_video(self):
        cam_list = self.findChild(QListWidget, 'cam_list')
        vid_list = self.findChild(QListWidget, 'vid_list')
        cam = cam_list.selectedItems()
        vid = vid_list.selectedItems()
        if cam and vid:
            cam_name = cam[0].text()
            vid_name = vid[0].text()
            vid_list.takeItem(vid_list.row(vid_list.selectedItems()[0]))
            path = f'{self.dir_path}\\Cameras\\{cam_name}\\videos\\{vid_name}'
            if os.path.exists(path):
                shutil.rmtree(path)

    def add_video_frames(self):
        cam = self.get_sel_cam()
        vid_list = self.findChild(QListWidget, 'vid_list')
        vid = vid_list.selectedItems()
        if cam and vid:
            cam_name = cam.text()
            vid_name = vid[0].text()

            path = f'{self.dir_path}\\Cameras\\{cam_name}\\videos\\{vid_name}'

            frames = []
            if path:
                count = 0
                per_sec = self.findChild(QtWidgets.QCheckBox, 'all').isChecked()
                for frame in os.listdir(path):
                    if not per_sec:
                        if count == 24:
                            frames.append(cv.imread(path + '\\' + frame))
                            count = 0
                    else:
                        frames.append(cv.imread(path + '\\' + frame))
                    count += 1

                if frames:
                    count = len(frames)
                    dialog = ImagesDialog(frames)
                    dialog.exec()
                    selected_frames = dialog.selected_frames

                    if selected_frames:
                        for i in range(count):
                            if selected_frames[i]:
                                frame_path = self.dir_path + '\\cameras\\' + cam_name + '\\frames\\%d_%s.jpg' % (
                                    i + 1, vid_name)
                                if not os.path.exists(frame_path):
                                    cv.imwrite(frame_path, frames[i])

                self.clear_list("frames_list")
                self.collect_data(f'\\cameras\\{cam_name}\\frames', "frames_list")

    def add_frame(self):
        cam = self.get_sel_cam()
        if cam:
            cam_name = cam.text()
            path = \
                QFileDialog.getOpenFileName(self, "Выберите изображение", "C:\\", "Image Files (*.jpg *.png *.jpeg)")[0]
            if path:
                frame_path = self.dir_path + '\\cameras\\' + cam_name + '\\frames\\' + path[path.rfind('/') + 1:]
                shutil.copy(path, frame_path)
                self.collect_data(f'\\cameras\\{cam_name}\\frames', "frames_list")

    def delete_frame(self, all=False):
        cam = self.get_sel_cam()
        if cam is not None:
            frames_list = self.findChild(QListWidget, 'frames_list')
            cam_name = cam.text()
            if all:
                path = f'{self.dir_path}\\cameras\\{cam_name}\\frames'
                if os.path.exists(path):
                    shutil.rmtree(path)
                    self.create_dir(f'{self.dir_path}\\cameras\\{cam_name}', 'frames')
            else:
                if frames_list.selectedItems():
                    frame_name = frames_list.selectedItems()[0].text()
                    frames_list.takeItem(frames_list.row(frames_list.selectedItems()[0]))
                    path = f'{self.dir_path}\\cameras\\{cam_name}\\frames\\{frame_name}'
                    if os.path.exists(path):
                        os.remove(path)

    def collect_data(self, path, list_widget_name):
        list_widget = self.findChild(QListWidget, list_widget_name)
        for dir in os.listdir(self.dir_path + path):
            item = QListWidgetItem(dir)
            list_widget.addItem(item)

    def cam_thread(self, method, vid_name=None, path_in=None, per_sec=None, width=None):
        cam = self.get_sel_cam()
        if cam is not None:
            cam_name = cam.text()
            self.thread_dict[cam_name] = []
            self.thread_dict[cam_name].append(QThread())
            calibrator = Calibrator(cam_name, self.dir_path)
            calibrator.get_results()
            self.thread_dict[cam_name].append(calibrator)

            self.thread_dict[cam_name][1].moveToThread(self.thread_dict[cam_name][0])

            if method == 'start':
                self.thread_dict[cam_name][0].started.connect(self.thread_dict[cam_name][1].start)
            if method == 'undistort_video':
                self.thread_dict[cam_name][0].started.connect(partial(self.thread_dict[cam_name][1].undistort_video, vid_name))
            if method == 'extract_images':
                self.thread_dict[cam_name][0].started.connect(partial(self.thread_dict[cam_name][1].extract_images, path_in, per_sec, cam_name, vid_name, width=width))

            self.thread_dict[cam_name][1].finished.connect(self.thread_dict[cam_name][0].quit)
            self.thread_dict[cam_name][1].finished.connect(self.thread_dict[cam_name][1].deleteLater)
            self.thread_dict[cam_name][0].finished.connect(self.thread_dict[cam_name][0].deleteLater)

            self.thread_dict[cam_name][1].progress.connect(partial(self.report_progress, cam_name))  # процесс выполнения потока

            self.thread_dict[cam_name][0].start()

            self.findChild(QPushButton, 'add_video').setEnabled(False)
            self.findChild(QPushButton, 'calibration').setEnabled(False)
            self.findChild(QPushButton, 'undistortion').setEnabled(False)
            self.thread_dict[cam_name][0].finished.connect(partial(self.finish_thread, cam_name))

    def calibrate_cam(self):
        self.cam_thread('start')

    def undistortion(self):
        vid = self.findChild(QListWidget, 'vid_list').selectedItems()
        if vid:
            self.cam_thread('undistort_video', vid_name=vid[0].text())

    def extract(self, path_in, per_sec, vid_name, width=None):
        self.cam_thread('extract_images', path_in=path_in, per_sec=per_sec, vid_name=vid_name, width=width)

    def finish_thread(self, cam_name):
        self.thread_dict.pop(cam_name)
        cam = self.get_sel_cam()

        if cam and cam_name == cam.text():
            self.clear_list("vid_list")
            self.collect_data(f'\\cameras\\{cam_name}\\videos', "vid_list")
            self.findChild(QPushButton, 'calibration').setEnabled(True)
            self.findChild(QPushButton, 'undistortion').setEnabled(True)
            self.findChild(QPushButton, 'add_video').setEnabled(True)
            progressbar = self.findChild(QtWidgets.QProgressBar, 'progressBar').setProperty("value", 0)

    def show_corners(self):
        self.show_images('corners')

    def show_undistortions(self):
        vid = self.findChild(QListWidget, 'vid_list').selectedItems()
        if vid:
            self.show_images('undistortions\\'+vid[0].text())

    def show_images(self, folder):
        frames = []
        cam = self.get_sel_cam()
        if cam is not None:
            cam_name = cam.text()
            img_path = f'{self.dir_path}\\cameras\\{cam_name}\\{folder}'
            if os.path.exists(img_path):
                for im_name in os.listdir(img_path):
                    img = cv.imread(img_path + '\\' + im_name)
                    frames.append(img)
                if frames:
                    dialog = ImagesDialog(frames, show=True)
                    dialog.exec()

    def report_progress(self, cam_name, n, n_max):
        progressbar = self.findChild(QtWidgets.QProgressBar, 'progressBar')
        cam = self.get_sel_cam()
        if cam.text() == cam_name:
            progressbar.setProperty("value", int(n/n_max*100))
