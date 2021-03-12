from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTextEdit, QPushButton, QProgressBar
from PyQt5.QtCore import Qt,QThread
from PyQt5.QtGui import QPalette, QIcon, QColor
from PyQt5.QtCore import QBasicTimer
import sys, os
import qtawesome
import translate_go
from tuozhuai import DropLineEdit

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
# dirname = os.path.dirname(PySide2.__file__)
# plugin_path = os.path.join(dirname, 'plugins', 'platforms')
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

class EmittingStr(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.textWritten.emit(str(text))
        '''
        loop = QEventLoop()
        QTimer.singleShot(1000, loop.quit)
        loop.exec_()
'''


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.lineEdit_1 = DropLineEdit(self)
        self.lineEdit_1.move(50,410)
        self.lineEdit_1.resize(200,21)
        self.lineEdit_2 = DropLineEdit(self)
        self.lineEdit_2.move(630,410)
        self.lineEdit_2.resize(200, 21)
        self.text = QTextEdit(self)
        self.text.move(0, 450)
        self.text.resize(1000, 800)
        self.setFixedSize(self.width() * 1.4, self.height() * 1.4)  # 禁止窗口拖动改变大小
        self.setupUi(self)
        # 下面将输出重定向到textBrowser中
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)

        self.btn.clicked.connect(self.bClicked)

    def msg(self):                     #选择文件夹
        self.directory_input = QtWidgets.QFileDialog.getExistingDirectory(None,"选取文件夹","C:/")  # 起始路径
        self.lineEdit_1.setText(self.directory_input)

    def msg_1(self, Filepath):  # 选择文件夹并输出路径
        self.directory_output = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "C:/")  # 起始路径
        self.lineEdit_2.setText(self.directory_output)
    

    def clear(self):
        self.title1_edit.setText(" ")
    
    def login_1(self):
        self.text.setText("账号密码已输入,点击开始以运行软件")

    def outputWritten(self, text):
        cursor = self.text.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.text.setTextCursor(cursor)
        self.text.ensureCursorVisible()

    def bClicked(self):
        """Runs the main function."""
        print('\n已运行')

        self.printABCD()
        self.update()

        print("Task done")

    def printABCD(self):
        data_process = translate_go.AudioDialogueOutput(input_file=self.directory_input,
                                         output_file=self.directory_output,
                                         appid="603c57fe", secret_key="46b84801453d1cbf51f0532288c929a1")
        data_process.run()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(10, 0, 30, 30))
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_1.setStyleSheet("QPushButton{\n"
                                        "    background:#F76677;\n"
                                        "    color:white;\n"
                                        "    border-radius:15px;\n"
                                        "}\n"
                                        "QPushButton:hover{                    \n"
                                        "    background:red;\n"
                                        "}\n")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(60, 0, 30, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet("QPushButton{\n"
                                        "    background:#F7D674;\n"
                                        "    color:white;\n"
                                        "    border-radius:15px;\n"
                                        "}\n"
                                        "QPushButton:hover{                    \n"
                                        "    background:yellow;\n"
                                        "}\n")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(110, 0, 30, 30))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setStyleSheet("QPushButton{\n"
                                        "    background:#6DDF6D;\n"
                                        "    color:white;\n"
                                        "    border-radius:15px;\n"
                                        "}\n"
                                        "QPushButton:hover{                    \n"
                                        "    background:green;\n"
                                        "}\n")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(100, 240, 100, 80))
        self.label_1.setObjectName("label_1")
        self.label_1.setStyleSheet(
            '''QLabel{color:rgb(10,10,10,255);font-size:20px;font-weight:bold;font-family:Roman times;}''')
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 40, 500, 80))
        self.label.setObjectName("label")
        self.label.setStyleSheet(
            '''QLabel{color:rgb(10,10,10,255);font-size:40px;font-weight:bold;font-family:Roman times;}''')
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(200, 120, 200, 80))
        self.title.setObjectName("title")
        self.title.setStyleSheet(
            '''QLabel{color:rgb(10,10,10,255);font-size:15px;font-weight:bold;font-family:Roman times;}''')
        self.title_1 = QtWidgets.QLabel(self.centralwidget)
        self.title_1.setGeometry(QtCore.QRect(200, 150, 200, 80))
        self.title_1.setObjectName("title_1")
        self.title_1.setStyleSheet(
            '''QLabel{color:rgb(10,10,10,255);font-size:15px;font-weight:bold;font-family:Roman times;}''')
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(630, 350, 100, 80))
        self.label_3.setObjectName("label_3")
        self.label_3.setStyleSheet(
            '''QLabel{color:rgb(10,10,10,255);font-size:20px;font-weight:bold;font-family:Roman times;}''')
        self.label1_3 = QtWidgets.QLabel(self.centralwidget)
        self.label1_3.setGeometry(QtCore.QRect(50, 350, 100, 80))
        self.label1_3.setObjectName("label1_3")
        self.label1_3.setStyleSheet('''QLabel{color:rgb(10,10,10,255);font-size:20px;font-weight:bold;font-family:Roman times;}''')
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(120, 620, 800, 40))
        self.label_4.setObjectName("label_4")
        self.label_4.setStyleSheet(
            '''QLabel{color:rgb(10,10,10,255);font-size:15px;font-weight:bold;font-family:Roman times;}''')
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(630, 260, 800, 40))
        self.label_5.setObjectName("label_5")
        self.label_5.setStyleSheet(
            '''QLabel{color:rgb(10,10,10,255);font-size:20px;font-weight:bold;font-family:Roman times;}''')
        self.warn_n = QtWidgets.QLabel(self.centralwidget)
        self.warn_n.setGeometry(QtCore.QRect(300, 360, 400, 80))
        self.warn_n.setObjectName("label")
        self.warn_n.setStyleSheet(
            '''QLabel{color:rgb(255,0,0,255);font-size:15px;font-weight:bold;font-family:Roman times;}''')
        self.title_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.title_edit.setGeometry(QtCore.QRect(380, 150, 200, 20))
        self.title_edit.setObjectName("title_edit")
        self.title_edit.setText('603c57fe')
        self.title1_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.title1_edit.setGeometry(QtCore.QRect(380, 180, 200, 21))
        self.title1_edit.setObjectName("title1_edit")
        self.title1_edit.setText('46b84801453d1cbf51f0532288c929a1')
        self.browse = QtWidgets.QPushButton(self.centralwidget)
        self.browse.setGeometry(QtCore.QRect(70, 320, 150, 40))
        self.browse.setMouseTracking(True)
        self.browse.setAcceptDrops(True)
        self.browse.setObjectName("browse")
        self.browse.setStyleSheet("QPushButton{\n"
                                  "    background:#1E90FF;\n"
                                  "    color:white;\n"
                                  "}\n"
                                  "QPushButton:hover{                    \n"
                                  "    background:#4169E1;\n"
                                  "}\n")
        self.browse_1 = QtWidgets.QPushButton(self.centralwidget)
        self.browse_1.setGeometry(QtCore.QRect(650, 320, 150, 40))
        self.browse_1.setMouseTracking(True)
        self.browse_1.setAcceptDrops(True)
        self.browse_1.setObjectName("browse_1")
        self.browse_1.setStyleSheet("QPushButton{\n"
                                    "    background:#1E90FF;\n"
                                    "    color:white;\n"
                                    "}\n"
                                    "QPushButton:hover{                    \n"
                                    "    background:#4169E1;\n"
                                    "}\n")
        self.login = QtWidgets.QPushButton(self.centralwidget)
        self.login.setGeometry(QtCore.QRect(480, 210, 100, 28))
        self.login.setMouseTracking(True)
        self.login.setAcceptDrops(True)
        self.login.setObjectName("login")
        self.login.setStyleSheet("QPushButton{\n"
                                 "    background:#1E90FF;\n"
                                 "    color:white;\n"
                                 "}\n"
                                 "QPushButton:hover{                    \n"
                                 "    background:#4169E1;\n"
                                 "}\n")
        self.reset = QtWidgets.QPushButton(self.centralwidget)
        self.reset.setGeometry(QtCore.QRect(380, 210, 100, 28))
        self.reset.setMouseTracking(True)
        self.reset.setAcceptDrops(True)
        self.reset.setObjectName("reset")
        self.reset.setStyleSheet("QPushButton{\n"
                                         "    background:#1E90FF;\n"
                                         "    color:white;\n"
                                         "}\n"
                                         "QPushButton:hover{                    \n"
                                         "    background:#4169E1;\n"
                                         "}\n")

        '''
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(330, 260, 93, 28))
        self.pushButton.setObjectName("pushButton")
        '''
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setWindowOpacity(0.9)  # 背景透明度
        pe = QPalette()
        MainWindow.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, QColor(237, 246, 251))  # 设置背景色
        MainWindow.setPalette(pe)
        self.browse.clicked.connect(self.msg)  # 鼠标点击按钮browse调用msg函数
        self.browse_1.clicked.connect(self.msg_1)  # 鼠标点击按钮调用msg_1函数
        self.reset.clicked.connect(self.clear)         #鼠标点击按钮调用clear函数
        self.login.clicked.connect(self.login_1)                #点击Login登录

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #self.pbar = QProgressBar(self)
        #self.pbar.setGeometry(330, 300, 200, 25)  # 设置进度条位置及大小
        self.btn = QPushButton('开始', self)
        # self.btn.move(50, 90)
        # self.btn.clicked.connect(self.doAction)  #点击按钮时执行的动作函数指定为self.doAction()
        self.btn.setGeometry(380, 300, 100, 40)
        self.btn.setStyleSheet("QPushButton{\n"
                               "    background:#778899;\n"
                               "    color:white;\n"
                               "    border-radius:15px;\n"
                               "}\n"
                               "QPushButton:hover{                    \n"
                               "    background:#4169E1;\n"
                               "}\n")
        self.timer = QBasicTimer()  # 构建一个计数器
        self.step = 0  # 设置基数

        # self.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mouth"))
        self.pushButton_1.setText(_translate("MainWindow", ""))
        self.pushButton_2.setText(_translate("MainWindow", ""))
        self.pushButton_3.setText(_translate("MainWindow", ""))
        self.label_1.setText(_translate("MainWindow", "选择文件"))
        self.label.setText(_translate("MainWindow", "中 英 文 唇 语 语 料 库"))
        self.title.setText(_translate("MainWindow", "科大讯飞appid"))
        self.title_1.setText(_translate("MainWindow", "科大讯飞secret key"))
        self.label_3.setText(_translate("MainWindow", "输出路径"))
        self.label1_3.setText(_translate("MainWindow", "输入路径"))
        self.label_4.setText(_translate("MainWindow", "本软件未购买科大讯飞商业服务，使用时长有限，请谨慎使用，或使用用户个人账户\n默认为作者本人账户（无需输入）"))
        self.warn_n.setText(_translate('MainWindow', '程序运行卡顿时间较长，请耐心等待'))
        self.label_5.setText(_translate("MainWindow", "请选择输出文件夹位置"))
        self.browse.setText(_translate("MainWindow", "browse_input"))
        self.browse_1.setText(_translate("MainWindow", "browse_output"))
        self.login.setText(_translate("MainWindow", "login"))
        self.reset.setText(_translate("MainWindow", "reset"))
        # self.pushButton.setText(_translate("MainWindow", "PushButton"))
        spin_icon = qtawesome.icon('fa5s.microphone-alt', color='black')
        MainWindow.setWindowIcon(spin_icon)

    def update(self):
        #self.btn.setText('输出过程较慢，请稍等。')
        self.cal = newThread()
        self.cal.start()

class newThread(QThread):
    def __init__(self):
        super(newThread, self).__init__()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widgets = Ui_MainWindow()
    # ui = Ui_MainWindow()
    # ui.setupUi(widgets)
    widgets.show()
    # ex=Ui_MainWindow()
    sys.exit(app.exec_())
