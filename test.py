import paramiko
import time


shortID = '8e5055c0'
domain = 'gravitel.aicall.ru'
ip = 'ssw.gravitel.ru'
user = 'nd'
password = '6aQtPZuLRz'
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
        ssh.recv(120).decode('utf8')
        message_to_ui = ssh.recv(10000000).decode('utf8')
except:
    message_to_ui = "Подключение не удалось"
print(message_to_ui)
