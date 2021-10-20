from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QLineEdit


class Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Добавление")
        self.setFixedSize(270, 120)
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.clicked.connect(self.get_cam_name)

        self.layout = QVBoxLayout()
        message = QLabel("Введите название камеры.")
        self.layout.addWidget(message)
        self.line_edit = QLineEdit(self)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def get_cam_name(self):
        self.name = self.line_edit.text()
