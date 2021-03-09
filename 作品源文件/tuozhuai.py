import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QPushButton,QLineEdit,QFileDialog

class DropLineEdit(QLineEdit):  #重写QLineEdit类--增加拖拽功能
    def __init__(self, parent=None):
        super(DropLineEdit, self).__init__(parent)
        #self.setAcceptDrops(True)   #是否接受拖放
        self.setDragEnabled(True)  # 拖拽是否启用
        #允许拖曳数据的控件必须设置QWidget.setDragEnabled()为True

    def dragEnterEvent(self, e):  #当拖动进入到控件区域时--事件
        #鼠标指针进入该控件时，这个事件将会被触发。在这个事件中可以获得被操作的窗口控件，还可以有条件地接受或拒绝该拖曳操作
        #通过e参数， 可取得QDragEnterEvent实例
        print('文件所有的路径',e.mimeData().urls())  # 文件所有的路径
        #[PyQt5.QtCore.QUrl('file:///D:/各种电影网地址.txt'), PyQt5.QtCore.QUrl('file:///D:/莱顿湖.jpg'), PyQt5.QtCore.QUrl('file:///D:/费南多.jpg')]
        #说明：拖动文件时可能同时拖动多个文件，返回值是列表--包含拖动的所有文件的路径

        print('文件路径',e.mimeData().text(),type(e.mimeData().text()))  # 文件路径
        #返回值类型str，【多个文件时，文件之间包含\n】
        #file:///D:/费南多.jpg
        #file:///D:/各种电影网地址.txt

        #print('支持的所有格式',e.mimeData().formats())  # 支持的所有格式

        #print(e.mimeData().data('text/plain'))  # 根据mime类型取路径 值为字节数组
        #b'file:///D:/\xe8\xb4\xb9\xe5\x8d\x97\xe5\xa4\x9a.jpg\nfile:///D:/\xe5\x90\x84\xe7\xa7\x8d\xe7\x94\xb5\xe5\xbd\xb1\xe7\xbd\x91\xe5\x9c\xb0\xe5\x9d\x80.txt\n'

        print(e.mimeData().hasText())  # 是否文本文件格式
        #True
        if e.mimeData().hasText():   #是否文本文件格式
            e.accept()   #是就接受--把文本在QLineEdit显示出来--文件路径显示出来
            #[在鼠标释放时接受]

        else:
            e.ignore()   #不是就忽略


class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.resize(500,300)
        self.setWindowTitle('实验室账盘点核对')
        self.wenjian_button=QPushButton('要核对的文件',self)
        self.wenjian_button.move(10, 10)
        self.wenjian_edit = DropLineEdit(self)
        self.wenjian_edit.move(100,10)
        self.wenjian_edit.resize(350,20)
        

    def wenjianbutton(self):
        r = QFileDialog.getOpenFileName(self, '请选择要打开的文件', './', 'All(*.*);;Excel(*.xlsx)',
                                        'Excel(*.xlsx)')
        self.wenjian_edit.setText(r[0])



if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())