import os
commands = "start/stop/exit"
status = 0
progress = 0
pro1 = "|>---------|"
pro2 = "|->--------|"
pro3 = "|-->-------|"
pro4 = "|--->------|"
pro5 = "|---->-----|"
pro6 = "|----->----|"
pro7 = "|------>---|"
pro8 = "|------->--|"
pro9 = "|-------->-|"
pro10 = "|--------->|"
continue_drive = "ja/nein", "weiterfahren?"
print(commands)
command = input()
if command == "start":
    status = 1
    print("ja/nein", "losfahren?")
    drive = input()
    if drive == "ja":
        status = 1
        progress = 1
        print(pro1)
        drive1 = input(continue_drive)
        if drive1 == "ja":
            status = 1
            progress = 2
            print(pro2)
            drive2 = input(continue_drive)
            if drive2 == "ja":
                status = 1
                progress = 3
                print(pro3)
                drive3 = input(continue_drive)
                if drive3 == "ja":
                    status = 1
                    progress = 4
                    print(pro4)
                    drive4 = input(continue_drive)
                    if drive4 == "ja":
                        status = 1
                        progress = 5
                        print(pro5)
                        drive5 = input(continue_drive)
                        if drive5 == "ja":
                            status = 1
                            progress = 6
                            print(pro6)
                            drive6 = input(continue_drive)
                            if drive6 == "ja":
                                status = 1
                                progress = 7
                                print(pro7)
                                drive7 = input(continue_drive)
                                if drive7 == "ja":
                                    status = 1
                                    progress = 8
                                    print(pro8)
                                    drive8 = input(continue_drive)
                                    if drive8 == "ja":
                                        status = 1
                                        progress = 9
                                        print(pro9)
                                        drive9 = input(continue_drive)
                                        if drive9 == "ja":
                                            status = 1
                                            progress = 10
                                            print(pro10)
                                            print("Du bist am Ziel.")
    if drive == "nein":
        status = 0
        command = input(commands)
if command == "stop" and status == 1:
    status = 0
if command == "stop" and status == 0:
    print("steht bereits")
if command == "exit" and status == 1 or status == 0:
    exit
