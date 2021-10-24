import os
import shutil
import cv2 as cv
import imutils
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QPushButton, QInputDialog, QFileDialog, QListWidget, QListWidgetItem
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from images_dialog import ImagesDialog
from calibrator import Calibrator


class MainWindow(QMainWindow):

    dir_path = os.getcwd()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Калибровка камер")
        self.setFixedSize(880, 660)
        centralwidget = QtWidgets.QWidget(self, objectName="centralwidget")
        # self.centralwidget.setObjectName("centralwidget")
        verticalLayoutWidget = QtWidgets.QWidget(centralwidget, objectName="verticalLayoutWidget")
        verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 293, 591))
        # verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        verticalLayout = QtWidgets.QVBoxLayout(verticalLayoutWidget)
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        # verticalLayout.setObjectName("verticalLayout")
        horizontalLayout = QtWidgets.QHBoxLayout()
        # horizontalLayout.setObjectName("horizontalLayout")

        pushButton = QPushButton(verticalLayoutWidget, text="Добавить камеру", objectName="create_cam")
        horizontalLayout.addWidget(pushButton)

        verticalLayout.addLayout(horizontalLayout)

        pushButton_2 = QPushButton(verticalLayoutWidget, text="Удалить камеру", objectName="delete_cam")
        horizontalLayout.addWidget(pushButton_2)

        list_widget = QListWidget(verticalLayoutWidget)
        list_widget.setObjectName("cam_list")
        verticalLayout.addWidget(list_widget)

        verticalLayoutWidget_2 = QtWidgets.QWidget(centralwidget)
        verticalLayoutWidget_2.setGeometry(QtCore.QRect(330, 10, 532, 591))
        verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")

        verticalLayout_2 = QtWidgets.QVBoxLayout(verticalLayoutWidget_2)
        verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        verticalLayout_2.setObjectName("verticalLayout_2")

        label = QtWidgets.QLabel(verticalLayoutWidget_2, text="Выберите камеру")
        label.setObjectName("cam_name")
        verticalLayout_2.addWidget(label)

        horizontalLayout_6 = QtWidgets.QHBoxLayout()
        horizontalLayout_6.setObjectName("horizontalLayout_6")

        verticalLayout_4 = QtWidgets.QVBoxLayout()
        verticalLayout_4.setObjectName("verticalLayout_4")

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

        pushButton_7 = QPushButton(verticalLayoutWidget_2, text="Углы", objectName='corners')
        verticalLayout_6.addWidget(pushButton_7)

        pushButton_9 = QPushButton(verticalLayoutWidget_2, text="Дисторции", objectName='undistortions')
        verticalLayout_6.addWidget(pushButton_9)

        pushButton_8 = QPushButton(verticalLayoutWidget_2, text="Выбрать кадры", objectName='choose_frames')
        verticalLayout_6.addWidget(pushButton_8)

        pushButton_13 = QPushButton(verticalLayoutWidget_2, text="Результаты", objectName='results')
        verticalLayout_6.addWidget(pushButton_13)

        horizontalLayout_6.addLayout(verticalLayout_6)
        verticalLayout_2.addLayout(horizontalLayout_6)

        progressBar = QtWidgets.QProgressBar(verticalLayoutWidget_2)
        progressBar.setProperty("value", 24)
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

        action = QtWidgets.QAction(self, text="Путь сохранения")
        action.setObjectName("action")
        menu.addAction(action),

        menubar.addAction(menu.menuAction())
        QtCore.QMetaObject.connectSlotsByName(self)
        self.set_logic()

    def set_logic(self):
        self.create_dir(self.dir_path, 'cameras')
        self.findChild(QPushButton, 'create_cam').clicked.connect(self.create_cam)
        self.findChild(QPushButton, 'delete_cam').clicked.connect(self.delete_cam)
        self.findChild(QPushButton, 'choose_frames').clicked.connect(self.add_video_frames)
        self.findChild(QPushButton, 'add_frame').clicked.connect(self.add_frame)
        self.findChild(QPushButton, 'delete_frame').clicked.connect(self.delete_frame)
        self.findChild(QPushButton, 'calibration').clicked.connect(self.calibrate_cam)
        self.findChild(QPushButton, 'corners').clicked.connect(self.show_corners)
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
            self.clear_list("frames_list")
            self.collect_data(f'\\cameras\\{cam_name}\\frames', "frames_list")

    def get_sel_cam(self):
        cam_list = self.findChild(QListWidget, 'cam_list')
        cam = None
        if cam_list.selectedItems():
            cam = cam_list.selectedItems()[0]
        return cam

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
                self.create_dir(f'{self.dir_path}\\cameras\\{cam_name}', 'frames')
                self.create_dir(f'{self.dir_path}\\cameras\\{cam_name}', 'results')
                self.create_dir(f'{self.dir_path}\\cameras\\{cam_name}', 'corners')
                self.create_dir(f'{self.dir_path}\\cameras\\{cam_name}', 'undistortions')

    def delete_cam(self):
        ########### Вы уверены, это удалит всю информацию о камере???
        cam_list = self.findChild(QListWidget, 'cam_list')
        cam = self.get_sel_cam()
        if cam is not None:
            cam_name = cam.text()
            cam_list.takeItem(cam_list.row(cam))
            path = self.dir_path + '\\cameras\\' + cam_name
            if os.path.exists(path):
                shutil.rmtree(path)
            label = self.findChild(QtWidgets.QLabel, 'cam_name')
            if label.text() == cam_name:
                self.clear_list("frames_list")
                label.setText('Выберите камеру')

    def add_video_frames(self):
        cam = self.get_sel_cam()
        if cam:
            path = QFileDialog.getOpenFileName(self, "Выберите видео", "C:/", "Video Files (*.mp4 *.avi *.mkv *.mpg)")[0]
            cam_name = cam.text()
            if path:
                vid_name = path[path.rfind('/') + 1:path.rfind('.')]
                calibrator = Calibrator(cam_name, self.dir_path)
                frames = calibrator.extract_images(path)
                dialog = ImagesDialog(frames)
                dialog.exec()
                if dialog.selected_frames:
                    for i in range(len(frames)):
                        if dialog.selected_frames[i]:
                            frame_path = self.dir_path + '\\cameras\\' + cam_name + '\\frames\\%d_%s.jpg' % (i+1, vid_name)
                            if not os.path.exists(frame_path):
                                cv.imwrite(frame_path, frames[i])
                    self.clear_list("frames_list")
                    self.collect_data(f'\\cameras\\{cam_name}\\frames', "frames_list")
        else:
            print('Error')

    def add_frame(self):
        cam = self.get_sel_cam()
        if cam:
            cam_name = cam.text()
            path = QFileDialog.getOpenFileName(self, "Выберите изображение", "C:\\", "Image Files (*.jpg *.png *.jpeg)")[0]
            if path:
                frame_path = self.dir_path + '\\cameras\\' + cam_name + '\\frames\\' + path[path.rfind('/') + 1:]
                shutil.copy(path, frame_path)
                self.collect_data(f'\\cameras\\{cam_name}\\frames', "frames_list")
        else:
            print('Error')

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

    def show_results(self):
        # path = f'\\cameras\\{cam_name}\\results'
        None

    def calibrate_cam(self):
        cam = self.get_sel_cam()
        cam_name = cam.text()
        if cam is not None:
            objpoints = []
            imgpoints = []
            calibrator = Calibrator(cam_name, self.dir_path)
            calibrator.draw_corners(objpoints, imgpoints)
            # calibrator.calibrate()
            # calibrator.undistort()
            # calibrator.re_projection_error()

    def show_corners(self):
        self.show_images('corners')

    def show_undistortions(self):
        self.show_images('undistortions')

    def show_images(self, folder):
        frames = []
        cam = self.get_sel_cam()
        if cam is not None:
            cam_name = cam.text()
            img_path = f'{self.dir_path}\\cameras\\{cam_name}\\{folder}'
            for im_name in os.listdir(img_path):
                img = cv.imread(img_path + '\\' + im_name)
                frames.append(img)
            dialog = ImagesDialog(frames, show=True)
            dialog.exec()
