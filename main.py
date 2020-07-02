import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design1
import paramiko
import time


class ExampleApp(QtWidgets.QMainWindow, design1.Ui_Dialog):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.connectButton.pressed.connect(self.connectUI)
        self.foundID.pressed.connect(self.foundIDSHH)
        self.ip = self.domainSSH.text()
        self.user = self.loginSSH.text()
        self.password = self.passwordSSH.text()
        self.port = 8023

    def output_message(self, message_to_ui):
        self.outputWindow.setText(message_to_ui)

    def connectUI(self):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                hostname=self.ip,
                username=self.user,
                password=self.password,
                port=self.port,
                look_for_keys=False)
            with client.invoke_shell() as ssh:
                time.sleep(0.5)
                print(ssh.recv(300).decode('utf8'))
            message_to_ui = "Подключение удалось."
        except:
            message_to_ui = "Не правильно введен логин, пароль или домен."

        self.output_message(message_to_ui)

    def foundIDSHH(self):
        number = self.numberSSH.text()
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                hostname=self.ip,
                username=self.user,
                password=self.password,
                port=self.port,
                look_for_keys=False)
            with client.invoke_shell() as ssh:
                time.sleep(0.5)
                print(ssh.recv(300).decode('utf8'))
            message_to_ui = "Подключение удалось."
        except:
            message_to_ui = "Не правильно введен логин, пароль или домен."



def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
