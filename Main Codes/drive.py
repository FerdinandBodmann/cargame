import os

commands = "start/stop/exit"
status = 0
progress = 0

progress_bars = [
    "|>---------|",
    "|->--------|",
    "|-->-------|",
    "|--->------|",
    "|---->-----|",
    "|----->----|",
    "|------>---|",
    "|------->--|",
    "|-------->-|",
    "|--------->|",
]

while True:
    print(commands)
    command = input()

    if command == "exit":
        break

    if command == "start":
        if status == 1:
            print("läuft bereits")
            continue
        status = 1
        progress = 0
        print("ja/nein | losfahren?")
        drive = input()
        if drive == "nein":
            status = 0
            continue
        while drive == "ja" and progress < 10:
            progress += 1
            print(progress_bars[progress - 1])
            if progress < 10:
                drive = input("ja/nein | weiterfahren? ")
        status = 0

    elif command == "stop":
        if status == 0:
            print("steht bereits")
        else:
            status = 0
