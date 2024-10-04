# import subprocess
# import send_png

#Pour installer kitty avec un envirronement Linux ou MacOS : https://sw.kovidgoyal.net/kitty/binary/
#kitten icat image.jpg dans le terminal kitty pour tester si ça marche

proc = subprocess.Popen('cmd.exe', stdin = subprocess.PIPE, stdout = subprocess.PIPE)
stdin, stdout = proc.communicate('chmod +x send-png')
stdin, stdout = proc.communicate('./send-png file.png')
