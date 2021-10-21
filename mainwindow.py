import os
import shutil

from PyQt5.QtWidgets import QMainWindow, QPushButton, QInputDialog
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from camera import Camera


class MainWindow(QMainWindow):
    cam_lst = []
    vid_lst = []
    frames_lst = []
    dir_path = os.getcwd()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Калибровка камер")
        self.setFixedSize(880, 660)
        self.centralwidget = QtWidgets.QWidget(self, objectName="centralwidget")
        # self.centralwidget.setObjectName("centralwidget")
        verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget, objectName="verticalLayoutWidget")
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

        listWidget = QtWidgets.QListWidget(verticalLayoutWidget)
        listWidget.setObjectName("cam_list")
        verticalLayout.addWidget(listWidget)

        verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        verticalLayoutWidget_2.setGeometry(QtCore.QRect(330, 10, 532, 591))
        verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")

        verticalLayout_2 = QtWidgets.QVBoxLayout(verticalLayoutWidget_2)
        verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        verticalLayout_2.setObjectName("verticalLayout_2")

        label = QtWidgets.QLabel(verticalLayoutWidget_2, text="Название камеры")
        label.setObjectName("cam_name")
        verticalLayout_2.addWidget(label)

        horizontalLayout_6 = QtWidgets.QHBoxLayout()
        horizontalLayout_6.setObjectName("horizontalLayout_6")

        verticalLayout_4 = QtWidgets.QVBoxLayout()
        verticalLayout_4.setObjectName("verticalLayout_4")

        horizontalLayout_5 = QtWidgets.QHBoxLayout()
        horizontalLayout_5.setObjectName("horizontalLayout_5")

        pushButton_5 = QPushButton(verticalLayoutWidget_2, text="Добавить видео")
        pushButton_5.setObjectName("pushButton_5")
        horizontalLayout_5.addWidget(pushButton_5)

        pushButton_6 = QPushButton(verticalLayoutWidget_2, text="Удалить видео")
        pushButton_6.setObjectName("pushButton_6")
        horizontalLayout_5.addWidget(pushButton_6)

        verticalLayout_4.addLayout(horizontalLayout_5)

        listWidget_3 = QtWidgets.QListWidget(verticalLayoutWidget_2)
        listWidget_3.setObjectName("listWidget_3")

        verticalLayout_4.addWidget(listWidget_3)

        horizontalLayout_6.addLayout(verticalLayout_4)

        verticalLayout_7 = QtWidgets.QVBoxLayout()
        verticalLayout_7.setObjectName("verticalLayout_7")
        horizontalLayout_7 = QtWidgets.QHBoxLayout()
        horizontalLayout_7.setObjectName("horizontalLayout_7")

        pushButton_11 = QPushButton(verticalLayoutWidget_2, text="Добавить кадр")
        pushButton_11.setObjectName("pushButton_11")
        horizontalLayout_7.addWidget(pushButton_11)

        pushButton_12 = QPushButton(verticalLayoutWidget_2, text="Удалить кадр")
        pushButton_12.setObjectName("pushButton_12")
        horizontalLayout_7.addWidget(pushButton_12)

        verticalLayout_7.addLayout(horizontalLayout_7)

        listWidget_4 = QtWidgets.QListWidget(verticalLayoutWidget_2)
        listWidget_4.setObjectName("listWidget_4")

        verticalLayout_7.addWidget(listWidget_4)

        horizontalLayout_6.addLayout(verticalLayout_7)

        verticalLayout_6 = QtWidgets.QVBoxLayout()
        verticalLayout_6.setObjectName("verticalLayout_6")

        pushButton_7 = QPushButton(verticalLayoutWidget_2, text="Углы")
        pushButton_7.setObjectName("pushButton_7")
        verticalLayout_6.addWidget(pushButton_7)

        pushButton_9 = QPushButton(verticalLayoutWidget_2, text="Дисторции")
        pushButton_9.setObjectName("pushButton_9")
        verticalLayout_6.addWidget(pushButton_9)

        pushButton_8 = QPushButton(verticalLayoutWidget_2, text="Выбрать кадры")
        pushButton_8.setObjectName("pushButton_8")
        verticalLayout_6.addWidget(pushButton_8)

        pushButton_13 = QPushButton(verticalLayoutWidget_2, text="Результаты")
        pushButton_13.setObjectName("pushButton_8")
        verticalLayout_6.addWidget(pushButton_13)

        horizontalLayout_6.addLayout(verticalLayout_6)
        verticalLayout_2.addLayout(horizontalLayout_6)

        progressBar = QtWidgets.QProgressBar(verticalLayoutWidget_2)
        progressBar.setProperty("value", 24)
        progressBar.setObjectName("progressBar")
        verticalLayout_2.addWidget(progressBar)

        pushButton_10 = QPushButton(verticalLayoutWidget_2, text="Калибровка")
        pushButton_10.setObjectName("pushButton_10")
        verticalLayout_2.addWidget(pushButton_10)

        MainWindow.setCentralWidget(self, self.centralwidget)

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
        menu.addAction(action)

        menubar.addAction(menu.menuAction())
        QtCore.QMetaObject.connectSlotsByName(self)
        self.set_data()

    def set_data(self):
        self.create_dir(self.dir_path, 'Cameras')
        self.findChild(QPushButton, 'create_cam').clicked.connect(self.create_cam)
        self.findChild(QPushButton, 'delete_cam').clicked.connect(self.delete_cam)
        listWidget_3 = self.findChild(QtWidgets.QListWidget, 'cam_list')
        label = self.findChild(QtWidgets.QLabel, 'cam_name')
        self.collect_data('\\Cameras', "cam_list")
        if listWidget_3.item(0):
            cam_name = listWidget_3.item(0).text()
            label.setText(cam_name)
            self.collect_data(f'\\Cameras\\{cam_name}\\videos', "listWidget_3")
            self.collect_data(f'\\Cameras\\{cam_name}\\frames', "listWidget_3")

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
        if cam_name is not None and dlg.result():
            if cam_name not in [cam.cam_name for cam in self.cam_lst] and cam_name != '':
                item = QtWidgets.QListWidgetItem(cam_name)
                self.findChild(QtWidgets.QListWidget, 'cam_list').addItem(item)

                new_cam = Camera(cam_name)
                self.cam_lst.append(new_cam)
                self.create_dir(self.dir_path + '\\Cameras', cam_name)
                self.create_dir(f'{self.dir_path}\\Cameras\\{cam_name}', 'videos')
                self.create_dir(f'{self.dir_path}\\Cameras\\{cam_name}', 'frames')
                self.create_dir(f'{self.dir_path}\\Cameras\\{cam_name}', 'results')
                self.create_dir(f'{self.dir_path}\\Cameras\\{cam_name}', 'corners')
                self.create_dir(f'{self.dir_path}\\Cameras\\{cam_name}', 'undistortions')

    def delete_cam(self):
        ########### Вы уверены, это удалит всю информацию о камере???
        cam_list = self.findChild(QtWidgets.QListWidget, 'cam_list')
        cam_name = cam_list.selectedItems()[0].text()
        cam_list.takeItem(cam_list.row(cam_list.selectedItems()[0]))
        path = self.dir_path + '\\Cameras\\' + cam_name
        if os.path.exists(path):
            shutil.rmtree(path)

    def add_video(self):
        None

    def delete_video(self):
        None

    def show_corners(self):
        None

    def show_undistortions(self):
        None

    def calibrate_cam(self):
        None

    def collect_data(self, path, list_widget_name):
        list_widget = self.findChild(QtWidgets.QListWidget, list_widget_name)
        for dir in os.listdir(self.dir_path + path):
            item = QtWidgets.QListWidgetItem(dir)
            list_widget.addItem(item)

    def load_cam_data(self, cam_name):
        None
