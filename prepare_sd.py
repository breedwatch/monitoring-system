import paramiko
import time
import subprocess

address = "192.168.2.176"
while True:
    try:
        res = subprocess.call(['ping', '-c', '3', address])
        if res == 0:
            ssh = paramiko.SSHClient()
            k = paramiko.RSAKey.from_private_key_file("/home/anderswodenker/.ssh/id_rsa")
            # OR k = paramiko.DSSKey.from_private_key_file(keyfilename)

            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect("192.168.2.176", username="pi", password="beemorocks", pkey=k)
            test_stdin, test_stdout, test_stderr = ssh.exec_command('sudo rm /home/pi/update.sh')
            for line in test_stdout.read().splitlines():
                print(line)

            ftp_client = ssh.open_sftp()
            ftp_client.put("/home/anderswodenker/Dev/monitoring-system/update.sh", "/home/pi/update.sh")
            ftp_client.close()

            test2_stdin, test2_stdout, test2_stderr = ssh.exec_command('sudo chmod 777 /home/pi/update.sh')
            for line in test2_stdout.read().splitlines():
                print(line)

            stdin, stdout, stderr = ssh.exec_command('sudo sh /home/pi/update.sh')

            for line in stdout.read().splitlines():
                print(line)

            ssh.exec_command('sudo shutdown now')
            ssh.close()
            more = input("WEITER GEHTS?")
    except Exception as e:
        print("FEHLER!")
        print(e)
        continue
    time.sleep(2)




