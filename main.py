import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5 import sip
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
        self.pushButton.pressed.connect(self.foundShortID)

    def output_message(self, message_to_ui):
        self.outputWindow.setText(message_to_ui)

    def connectUI(self):
        ip = self.domainSSH.text()
        user = self.loginSSH.text()
        password = self.passwordSSH.text()
        port = 8023
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                hostname=ip,
                username=user,
                password=password,
                port=port,
                look_for_keys=False)
            with client.invoke_shell() as ssh:
                time.sleep(0.5)
                print(ssh.recv(1000).decode('utf8'))
            message_to_ui = "Подключение удалось."
        except:
            message_to_ui = "Не правильно введен логин, пароль или домен."

        self.output_message(message_to_ui)

    def foundIDSHH(self):
        number = self.numberSSH.text()
        domain = self.foundDomainSSH.text()
        ip = self.domainSSH.text()
        user = self.loginSSH.text()
        password = self.passwordSSH.text()
        port = 8023
        send_mes = 'domain/' + domain + '/trace/list --addr ' + number + '\n'
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                hostname=ip,
                username=user,
                password=password,
                port=port,
                look_for_keys=False)
            with client.invoke_shell() as ssh:
                ssh.send(send_mes)
                time.sleep(0.5)
            message_to_ui = ssh.recv(10000).decode('utf8')
        except:
            message_to_ui = "Подключение не удалось"
        self.output_message(message_to_ui)

    def foundShortID(self):
        shortID = self.shortID.text()
        domain = self.foundDomainSSH.text()
        ip = self.domainSSH.text()
        user = self.loginSSH.text()
        password = self.passwordSSH.text()
        port = 8023
        send_mes = 'domain/' + domain + '/trace/show --Te ' + shortID + ' --payload\n'
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                hostname=ip,
                username=user,
                password=password,
                port=port,
                look_for_keys=False)
            with client.invoke_shell() as ssh:
                ssh.send(send_mes)
                time.sleep(0.5)
                '''ssh.recv(120).decode('utf8')'''
                message_to_ui = ssh.recv(10000000).decode("utf-8")
                file = open('log-' + time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()) + '.txt', 'w')
                file.write(''.join(message_to_ui))
                file.close()
        except:
            message_to_ui = "Подключение не удалось"
        print(message_to_ui)
        self.output_message(message_to_ui)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
