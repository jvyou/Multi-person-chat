from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import *
from First1 import Ui_MainWindow
from Second1 import Ui_MainWindow2
from Third1 import Ui_MainWindow3
from Fourth1 import Ui_MainWindow4
from Main1 import Ui_MainWindow5
import tkinter as tk
from tkinter import filedialog  # 获取文件
import sys
import pymssql  # 数据库
from socket import *  # 网络
from threading import Thread  # 多线程

db = pymssql.connect(host='localhost',user='sa',password='1739015622',database='wangzhe',charset='utf8')
cur = db.cursor()


class First(Ui_MainWindow,QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.login)
        self.pushButton_4.clicked.connect(self.register)
        self.pushButton_5.clicked.connect(self.alter)
        self.pushButton_6.clicked.connect(self.back)
        btn = self.pushButton_3
        btn.setShortcut('enter')

    def login(self):
        useres=self.lineEdit.text()
        password=self.lineEdit_2.text()
        sql="select * from users"
        cur.execute(sql)
        all_row = cur.fetchall()
        flag = 1
        for i in range(len(all_row)):
            if all_row[i][0] == useres and all_row[i][1] == password:
                reply = QMessageBox.information(self, '标题', '登录成功，欢迎使用！',
                                                QMessageBox.Ok)  # 信息框
                id_w=all_row[i][2]
                tou_w=all_row[i][3]
                self.close()
                self.main = Main(useres,password,id_w,tou_w)
                self.main.show()
                flag = 0
                break
        if flag == 1:
            reply = QMessageBox.information(self, '标题', '用户名或密码不对，登录失败！',
                                            QMessageBox.Ok)  # 信息框
            return False

    def register(self):
        self.second=Second()
        self.second.show()

    def alter(self):
        self.third=Third()
        self.third.show()

    def back(self):
        self.fourth=Fourth()
        self.fourth.show()


class Second(Ui_MainWindow2,QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.registers)

    def registers(self):
        useres = self.lineEdit.text()
        password = self.lineEdit_2.text()
        password_s = self.lineEdit_3.text()
        id = self.lineEdit_4.text()
        tou='touxiang.jpg'
        if useres == '':
            reply = QMessageBox.information(self, '标题', '用户名不许为空，注册失败！',
                                            QMessageBox.Ok)  # 信息框
            return False
        if password == '' or password_s == '':
            reply = QMessageBox.information(self, '标题', '密码不许为空，注册失败！',
                                            QMessageBox.Ok)  # 信息框
            return False
        if id == '':
            reply = QMessageBox.information(self, '标题', '昵称不许为空，注册失败！',
                                            QMessageBox.Ok)  # 信息框
            return False
        if password != password_s:
            reply = QMessageBox.information(self, '标题', '密码和确认密码不一致，注册失败！',
                                            QMessageBox.Ok)  # 信息框
            return False
        try:
            sql="insert into users values('%s','%s','%s','%s')" % (useres,password,id,tou)
            cur.execute(sql)
            db.commit()
            reply = QMessageBox.information(self, '标题', '注册成功！',
                                        QMessageBox.Ok)  # 信息框
            self.close()
        except:
            reply = QMessageBox.information(self, '标题', '用户名不允许重复，注册失败！',
                                            QMessageBox.Ok)  # 信息框
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            return False


class Third(Ui_MainWindow3,QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.alters)

    def alters(self):
        useres = self.lineEdit.text()
        password = self.lineEdit_2.text()
        password_s = self.lineEdit_3.text()
        if useres == '':
            reply = QMessageBox.information(self, '标题', '用户名不许为空，修改失败！',
                                            QMessageBox.Ok)  # 信息框
            return False
        if password == '' or password_s == '':
            reply = QMessageBox.information(self, '标题', '密码不许为空，修改失败！',
                                            QMessageBox.Ok)  # 信息框
            return False
        if password != password_s:
            reply = QMessageBox.information(self, '标题', '密码和确认密码不一致，修改失败！',
                                            QMessageBox.Ok)  # 信息框
            return False
        sql = "select * from users"
        cur.execute(sql)
        all_row = cur.fetchall()
        flag = 1
        for i in range(len(all_row)):
            if (all_row[i][0] == useres):
                sql_2 = "update users set password=('%s') where useres=('%s')" % (password,useres)
                cur.execute(sql_2)
                db.commit()
                reply = QMessageBox.information(self, '标题', '修改成功！',
                                            QMessageBox.Ok)  # 信息框
                self.close()
                flag=0
                break
        if flag==1:
            reply = QMessageBox.information(self, '标题', '未找到此用户名，修改失败！',
                                            QMessageBox.Ok)  # 信息框
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            return False


class Fourth(Ui_MainWindow4,QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.backs)

    def backs(self):
        useres = self.lineEdit.text()
        if useres == '':
            reply = QMessageBox.information(self, '标题', '用户名不许为空，找回失败！',
                                            QMessageBox.Ok)  # 信息框
            return False
        sql = "select * from users"
        cur.execute(sql)
        all_row = cur.fetchall()
        flag = 1
        for i in range(len(all_row)):
            if (all_row[i][0] == useres):
                self.lineEdit_2.setText(all_row[i][1])
                reply = QMessageBox.information(self, '标题', '找回成功！',
                                            QMessageBox.Ok)  # 信息框
                flag=0
                break
        if flag==1:
            reply = QMessageBox.information(self, '标题', '未找到此用户名，找回失败！',
                                            QMessageBox.Ok)  # 信息框
            self.lineEdit.clear()
            return False


class Main(Ui_MainWindow5,QtWidgets.QMainWindow,QInputDialog):
    def __init__(self,useres,password,id_w,tou_w):
        super().__init__()
        self.setupUi(self)
        self.id_w=id_w
        self.useres=useres
        self.password=password
        self.tou_w=tou_w
        pix = QtGui.QPixmap(f'{tou_w}')
        self.label_2.setPixmap(pix)
        self.label_2.setScaledContents(True)
        self.label_3.setText(id_w)
        self.pushButton_7.clicked.connect(self.changetou)
        self.pushButton_8.clicked.connect(self.changename)
        self.pushButton_9.clicked.connect(self.connect)
        self.pushButton_10.clicked.connect(self.sends)
        self.pushButton_11.clicked.connect(self.closes)
        btn=self.pushButton_10
        btn.setShortcut('enter')

    def changetou(self):
        root = tk.Tk()
        root.withdraw()
        Filepath = filedialog.askopenfilename()
        File=Filepath.split('/')
        Files=File[-1]
        self.tou_w=Files
        pix = QtGui.QPixmap(Files)
        self.label_2.setPixmap(pix)
        self.label_2.setScaledContents(True)
        sql = "update users set tou=('%s') where useres=('%s') and password=('%s')" % (Files,self.useres,self.password)
        cur.execute(sql)
        db.commit()
        QMessageBox.information(self, '标题', '更换成功！',
                                QMessageBox.Ok)  # 信息框

    def changename(self):
        inf,ok=QInputDialog.getText(self,'标题','请输入昵称:')
        self.label_3.setText(inf)
        self.id_w=inf
        sql = "update users set id=('%s') where useres=('%s') and password=('%s')" % (inf,self.useres,self.password)
        cur.execute(sql)
        db.commit()
        QMessageBox.information(self, '标题', '更换成功！',
                                QMessageBox.Ok)  # 信息框

    def connect(self):
        self.connfd = socket()
        server_addr = ('127.0.0.1', 8888)  # 服务器地址
        try:
            self.connfd.connect(server_addr)
            self.connfd.send(self.id_w.encode())
            self.textEdit_2.append('用户列表')
            QMessageBox.information(self, '标题', '连接成功！',
                                    QMessageBox.Ok)  # 信息框
        except:
            QtWidgets.QMessageBox.warning(self, "警告", "请确保服务器打开！！！")
            return False
        def recv():
            while True:
                try:
                    data=self.connfd.recv(1024).decode()
                    if data.split()[0]=='id':
                        self.textEdit_2.append(data.split()[1])
                    elif data.split()[0]=='系统消息：' and data.split()[2]=='离开了聊天室!':
                        #self.textEdit_2.clear()
                        self.textEdit.append(data)
                        self.textEdit_2.append('用户列表')
                    else:
                        self.textEdit.append(data)
                except:
                    break
        self.t=Thread(target=recv)
        self.t.start()

    def sends(self):
        try:
            msg = self.lineEdit.text()
            self.connfd.send(msg.encode())
            self.lineEdit.clear()
        except:
            QtWidgets.QMessageBox.warning(self, "警告", "请确保先连接服务器再发送消息！")
            return False

    def closes(self):
        try:
            self.connfd.close()
            self.t.join()
            self.textEdit.clear()
            self.textEdit_2.clear()
            QMessageBox.information(self, '标题', '断开成功！',
                                    QMessageBox.Ok)  # 信息框
        except:
            QtWidgets.QMessageBox.warning(self, "警告", "您还未连接，无法断开！")
            return False


QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
app=QtWidgets.QApplication(sys.argv)
first=First()
first.show()
sys.exit(app.exec_())
