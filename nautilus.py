from models import *
from config import *


def is_char_legal(cmd_line):
    for args in cmd_line:
        for char in args:
            if char not in VALID_CHARS:
                return False


def is_new_usr_exist_checker(target: str, existing_usr_list: list):
    is_new_usr_exist = False
    for i in existing_usr_list:
        if i.usr_name == target:
            is_new_usr_exist = True
    return is_new_usr_exist


def adduser(new_usr_name: str, new_current_folder: RootFolder):
    new_added_usr = User(usr_name=new_usr_name, current_folder=new_current_folder)
    return new_added_usr


def test_control():

    usr_root_folder = RootFolder("/", None)
    default_root_usr = User("root", usr_root_folder)

    current_running_usr = default_root_usr

    existing_usr_list = []  # contains usr objects
    existing_usr_list.append(current_running_usr)

    is_running = True
    while is_running:
        print(current_running_usr.usr_name + ":" + current_running_usr.pwd() + "$ ", end="")
        # cmd_line = input().replace("   ", " tab ").split(" ")
        cmd_line = input().strip().split(" ")
        # cmd_line = input().split(" ")

        if is_char_legal(cmd_line=cmd_line) == False:
            print(cmd_line[0] + ": Invalid syntax")
            continue

        if cmd_line[0] == "exit":
            if cmd_line[0] in cmd_line[1:]:
                print(cmd_line[0] + ": Invalid syntax")
                continue
            print("bye, " + current_running_usr.usr_name)
            is_running = False
            continue

        elif cmd_line[0] == "":
            continue

        elif cmd_line[0] == "\t\t" or cmd_line[0] == "\t":
            continue

        elif cmd_line[0] == "pwd":
            if "pwd" in cmd_line[1:]:
                print("pwd: Invalid syntax")
                continue
            print(current_running_usr.pwd())

        elif cmd_line[0] == "touch":
            if cmd_line[0] in cmd_line[1:]:
                print(cmd_line[0] + ": Invalid syntax")
                continue
            try:
                current_running_usr.touch(cmd_line[1].replace("\"", ""), current_running_usr)
            except:
                print(cmd_line[0] + ": Invalid syntax")

        elif cmd_line[0] == "ls":
            if cmd_line[0] in cmd_line[1:]:
                print(cmd_line[0] + ": Invalid syntax")
                continue
            # try:
            if "-l" not in cmd_line:
                current_running_usr.ls(obj_target_folder=current_running_usr.current_folder, is_l=False)
            else:
                current_running_usr.ls(obj_target_folder=current_running_usr.current_folder, is_l=True)
            # except:
            #     print(cmd_line[0] + ": Invalid syntax")

        elif cmd_line[0] == "mkdir":
            if cmd_line[0] in cmd_line[1:] or "-q" in cmd_line[1:]:
                print(cmd_line[0] + ": Invalid syntax")
                continue
            try:
                if ("-p" not in cmd_line) and ("-P" not in cmd_line):
                    current_running_usr.mkdir(cmd_line[1], False, current_running_usr=current_running_usr)
                if ("-p" in cmd_line) or ("-P" in cmd_line):
                    cmd_line.remove("-p")
                    current_running_usr.mkdir(cmd_line[1], True, current_running_usr=current_running_usr)
            except:
                print(cmd_line[0] + ": Invalid syntax")

        elif cmd_line[0] == "cd":
            if cmd_line[0] in cmd_line[1:]:
                print(cmd_line[0] + ": Invalid syntax")
                continue
            try:
                current_running_usr.cd(cmd_line[1])
            except:
                print(cmd_line[0] + ": Invalid syntax")

        elif cmd_line[0] == "cp":
            if cmd_line[0] in cmd_line[1:]:
                print(cmd_line[0] + ": Invalid syntax")
                continue
            try:
                current_running_usr.cp(src_path=cmd_line[1],
                                       dst_path=cmd_line[2],
                                       current_running_usr=current_running_usr)
            except:
                print(cmd_line[0] + ": Invalid syntax")

        elif cmd_line[0] == "mv":
            if cmd_line[0] in cmd_line[1:]:
                print(cmd_line[0] + ": Invalid syntax")
                continue
            try:
                current_running_usr.mv(src_path=cmd_line[1],
                                       dst_path=cmd_line[2],
                                       current_running_usr=current_running_usr)
            except:
                print(cmd_line[0] + ": Invalid syntax")

        elif cmd_line[0] == "rm":
            if cmd_line[0] in cmd_line[1:]:
                print(cmd_line[0] + ": Invalid syntax")
                continue
            try:
                current_running_usr.rm(cmd_line[1].replace("\"", ""))
            except:
                print(cmd_line[0] + ": Invalid syntax")

        elif cmd_line[0] == "rmdir":
            if cmd_line[0] in cmd_line[1:]:
                print(cmd_line[0] + ": Invalid syntax")
                continue
            try:
                current_running_usr.rmdir(cmd_line[1])
            except:
                print(cmd_line[0] + ": Invalid syntax")

        elif cmd_line[0] == "adduser":
            if current_running_usr.usr_name != "root":
                continue
            if is_new_usr_exist_checker(target=cmd_line[1], existing_usr_list=existing_usr_list):
                print("adduser: The user already exists")
                continue
            else:
                new_usr = adduser(new_usr_name=cmd_line[1], new_current_folder=usr_root_folder)
                existing_usr_list.append(new_usr)

        elif cmd_line[0] == "su":
            if len(cmd_line) == 1:
                current_running_usr = default_root_usr
                continue
            if not is_new_usr_exist_checker(target=cmd_line[1], existing_usr_list=existing_usr_list):
                print("su: Invalid user")
                continue
            else:
                for i in existing_usr_list:
                    if i.usr_name == cmd_line[1]:
                        current_running_usr = i

        elif cmd_line[0] == "deluser":
            if current_running_usr.usr_name != "root":
                continue
            if cmd_line[1] == "root":
                print("WARNING: You are just about to delete the root account")
                print("Usually this is never required as it may render the whole system unusable")
                print("If you really want this, call deluser with parameter --force")
                print("(but this `deluser` does not allow `--force`, haha)")
                print("Stopping now without having performed any action")
                continue
            if not is_new_usr_exist_checker(target=cmd_line[1], existing_usr_list=existing_usr_list):
                print("deluser: The user does not exist")
                continue
            else:
                for i in existing_usr_list:
                    if i.usr_name == cmd_line[1]:
                        existing_usr_list.remove(i)

        elif cmd_line[0] == "chown":
            if current_running_usr.usr_name != "root":
                print("chown: Operation not permitted")
                continue
            if not is_new_usr_exist_checker(target=cmd_line[1], existing_usr_list=existing_usr_list):
                print("chown: Invalid user")
                continue
            else:
                for i in existing_usr_list:
                    if i.usr_name == cmd_line[1]:
                        current_running_usr.chown(obj_new_owner=i, target=cmd_line[2])

        elif cmd_line[0] == "chmod":
            current_running_usr.chmod(str_usr_perms=cmd_line[1], str_target_path=cmd_line[2])

        else:
            print(cmd_line[0] + ": Command not found")


# test()
test_control()

