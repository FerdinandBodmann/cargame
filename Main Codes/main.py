import os
commands = "start/stop/exit"
status = 0
progress = 0

print(commands)
command = input()
if command == "start":
    status = 1
    print("ja/nein", "losfahren?")
    drive = input()
    if drive == "ja":
        status = 1
        progress = 1
    if drive == "nein":
        status = 0
if command == "stop" and status == 1:
    status = 0
if command == "stop" and status == 0:
    print("steht bereits")
if command == "exit" and status == 1 or status == 0:
    exit
