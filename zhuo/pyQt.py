import sys

from PyQt5 import QtWidgets

#创建一个应用(Application)对象,sys.argv参数是一个来自命令行的参数列表,

# Python脚本可以在shell中运行。这是我们用来控制我们应用启动的一种方法。

app = QtWidgets.QApplication(sys.argv)

#创建一个widget组件基础类

windows = QtWidgets.QWidget()

#设置widget组件的大小(w,h)

windows.resize(500,500)

#设置widget组件的位置(x,y)

windows.move(100,100)

"""

#设置widget组件的位置居中

qr = windows.frameGeometry()

cp = QtWidgets.QDesktopWidget().availableGeometry().center()

qr.moveCenter(cp)

windows.move(qr.topLeft())

"""

#等同于 w.resize(500,500)和w.move(100,100)两句结合,(x,y,w,h)

#windows.setGeometry(100,100,500,500)

#show()方法在屏幕上显示出widget组件

windows.show()

#循环执行窗口触发事件，结束后不留垃圾的退出，不添加的话新建的widget组件就会一闪而过

sys.exit(app.exec_())