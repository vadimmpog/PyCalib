from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets
import imutils


class ImagesDialog(QDialog):
    def __init__(self, frames, show=False):
        super().__init__()

        self.current_image = 0
        self.frames = frames
        self.frames_num = len(frames)
        self.show = show
        if not show:
            self.selected_frames = [False for _ in range(self.frames_num)]

        self.setWindowTitle("Добавление")
        self.setFixedSize(724, 519)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(480, 470, 211, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.label = QtWidgets.QLabel(self)
        self.label.setMargin(30)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(260, 430, 195, 80))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)

        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)

        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        if not show:
            self.checkBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
            self.checkBox.setObjectName("checkBox")
            self.gridLayout.addWidget(self.checkBox, 0, 1, 1, 1)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.set_logic()

    def set_logic(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle("Просмотр фреймов")
        self.label.setText("Пустой кадр")
        self.pushButton_2.setText(">>")
        self.pushButton_2.clicked.connect(self.next_image)
        self.pushButton.setText("<<")
        self.pushButton.clicked.connect(self.previous_image)
        if not self.show:
            self.checkBox.setText("выбрать")
            self.checkBox.clicked.connect(self.select_frame)
        self.choose_frames()

    def choose_frames(self, i=0):
        self.label_2.setText(f"{i + 1}/{self.frames_num}")
        image = imutils.resize(self.frames[i], width=550)
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pix = QPixmap.fromImage(qImg)
        self.label.setPixmap(pix)

    def next_image(self):
        if self.current_image < self.frames_num-1:
            self.current_image += 1
            self.choose_frames(i=self.current_image)
            if not self.show:
                self.checkBox.setChecked(self.selected_frames[self.current_image])

    def previous_image(self):
        if self.current_image > 0:
            self.current_image -= 1
            self.choose_frames(i=self.current_image)
            if not self.show:
                self.checkBox.setChecked(self.selected_frames[self.current_image])

    def select_frame(self):
        self.selected_frames[self.current_image] = not self.selected_frames[self.current_image]

    def reject(self):
        super().reject()
        if not self.show:
            self.selected_frames = None



