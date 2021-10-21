import os
import shutil

from PyQt5.QtWidgets import QMainWindow, QPushButton, QInputDialog, QFileDialog
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from camera import Camera


class MainWindow(QMainWindow):
    ####??????????????????
    cam_lst = []
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

        list_widget = QtWidgets.QListWidget(verticalLayoutWidget)
        list_widget.setObjectName("cam_list")
        verticalLayout.addWidget(list_widget)

        verticalLayoutWidget_2 = QtWidgets.QWidget(centralwidget)
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

        pushButton_5 = QPushButton(verticalLayoutWidget_2, text="Добавить видео", objectName='add_video')
        horizontalLayout_5.addWidget(pushButton_5)

        pushButton_6 = QPushButton(verticalLayoutWidget_2, text="Удалить видео", objectName='delete_video')
        horizontalLayout_5.addWidget(pushButton_6)

        verticalLayout_4.addLayout(horizontalLayout_5)

        list_widget_3 = QtWidgets.QListWidget(verticalLayoutWidget_2)
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

        list_widget_4 = QtWidgets.QListWidget(verticalLayoutWidget_2)
        list_widget_4.setObjectName("frames_list")

        verticalLayout_7.addWidget(list_widget_4)

        horizontalLayout_6.addLayout(verticalLayout_7)

        verticalLayout_6 = QtWidgets.QVBoxLayout()
        verticalLayout_6.setObjectName("verticalLayout_6")

        pushButton_7 = QPushButton(verticalLayoutWidget_2, text="Углы", objectName='corners')
        verticalLayout_6.addWidget(pushButton_7)

        pushButton_9 = QPushButton(verticalLayoutWidget_2, text="Дисторции", objectName='distortions')
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
        menu.addAction(action)

        menubar.addAction(menu.menuAction())
        QtCore.QMetaObject.connectSlotsByName(self)
        self.set_logic()

    def set_logic(self):
        self.create_dir(self.dir_path, 'Cameras')
        self.findChild(QPushButton, 'create_cam').clicked.connect(self.create_cam)
        self.findChild(QPushButton, 'delete_cam').clicked.connect(self.delete_cam)
        self.findChild(QPushButton, 'add_video').clicked.connect(self.add_video)
        self.findChild(QPushButton, 'delete_video').clicked.connect(self.delete_video)
        # self.findChild(QPushButton, 'add_frame').clicked.connect(self.add_frame)
        # self.findChild(QPushButton, 'delete_frame').clicked.connect(self.delete_frame)
        list_widget = self.findChild(QtWidgets.QListWidget, 'cam_list')
        list_widget.itemClicked.connect(self.set_cam_data)
        self.collect_data('\\Cameras', "cam_list")
#########
    def set_cam_data(self):
        list_widget = self.findChild(QtWidgets.QListWidget, 'cam_list')
        item = list_widget.selectedItems()[0]
        if item:
            cam_name = item.text()
            label = self.findChild(QtWidgets.QLabel, 'cam_name')
            label.setText(cam_name)
            self.clear_list("vid_list")
            self.clear_list("frames_list")
            self.collect_data(f'\\Cameras\\{cam_name}\\videos', "vid_list")
            self.collect_data(f'\\Cameras\\{cam_name}\\frames', "frames_list")

    def clear_list(self, list_name):
        list_widget = self.findChild(QtWidgets.QListWidget, list_name)
        list_widget.clear()

    def create_dir(self, path, name):
        abs_path = path + '\\' + name
        if not os.path.exists(abs_path):
            os.mkdir(abs_path)
#######
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

                new_cam = Camera(cam_name)#####
                self.cam_lst.append(new_cam) ### ???????????

                self.create_dir(self.dir_path + '\\Cameras', cam_name)
                self.create_dir(f'{self.dir_path}\\Cameras\\{cam_name}', 'videos')
                self.create_dir(f'{self.dir_path}\\Cameras\\{cam_name}', 'frames')
                self.create_dir(f'{self.dir_path}\\Cameras\\{cam_name}', 'results')
                self.create_dir(f'{self.dir_path}\\Cameras\\{cam_name}', 'corners')
                self.create_dir(f'{self.dir_path}\\Cameras\\{cam_name}', 'undistortions')
#######
    def delete_cam(self):
        ########### Вы уверены, это удалит всю информацию о камере???
        cam_list = self.findChild(QtWidgets.QListWidget, 'cam_list')
        cam_name = cam_list.selectedItems()[0].text()
        cam_list.takeItem(cam_list.row(cam_list.selectedItems()[0]))
        path = self.dir_path + '\\Cameras\\' + cam_name
        if os.path.exists(path):
            shutil.rmtree(path)
        label = self.findChild(QtWidgets.QLabel, 'cam_name')
        if label.text() == cam_name:
            self.clear_list("vid_list")
            self.clear_list("frames_list")
            label.setText('Название камеры')

    def add_video(self):
        list_widget = self.findChild(QtWidgets.QListWidget, 'cam_list')
        cam = list_widget.selectedItems()
        if cam:
            cam_name = cam[0].text()
            path = QFileDialog.getOpenFileName(self, "Выберите видео", "", "Video Files (*.mp4 *.avi)")[0]
            ### объект видео добавить в объект камеры?
            vid_name = path.split('/')[-1]
            self.create_dir(f'{self.dir_path}\\Cameras\\{cam_name}\\videos', vid_name)
            item = QtWidgets.QListWidgetItem(vid_name)
            self.findChild(QtWidgets.QListWidget, 'vid_list').addItem(item)
        else:
            print('Error')

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
