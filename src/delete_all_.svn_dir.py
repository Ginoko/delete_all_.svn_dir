"""
===========================
Delete All '.svn' Directory
===========================

:Date: 2021-06-02
:Version: 1.0.0
:Author: Ginoko
:Contact: ginorasakushisu666@gmail.com
"""
import os
import sys
import getopt
import platform

platform_is_windows = True
global_svn_dir_list = []


def detect_platform() -> None:
    global platform_is_windows
    system = platform.system()
    if system != "Windows":
        platform_is_windows = False


def show_help_msg():
    print("Usage: %s [OPTIONS]\n"
          "    OPTIONS:\n"
          "        -r ABSOLUTE-PATH use this path as the working root to find and delete all '.svn' directories\n"
          "        -h show this message" % os.path.split(__file__)[-1])


def read_root_config_from_argv(argv: list) -> str:
    root = os.getcwd()
    options, args = getopt.getopt(argv, "r:h", ["root=", "help"])
    for option, value in options:
        if option in ("-r", "--root"):
            root = str(value)
        if option in ("-h", "--help"):
            show_help_msg()
            exit(0)
    return root


def let_user_reenter_root_config() -> str:
    print("please enter the ABSOLUTE path you want to walk through...")
    while True:
        root = input("[ABSOLUTE path]: ")
        if not os.path.exists(root):
            print('the path "%s" dose not exist!' % root)
            print("PLEASE enter the EXISTING ABSOLUTE path you want to walk through...")
        else:
            return root


def let_user_confirm_the_root(project_root: str) -> str:
    root = project_root
    while True:
        confirm = input('using root "%s"? (Y/N): ' % project_root).lower()
        if confirm == "y":
            break
        elif confirm == "n":
            root = let_user_reenter_root_config()
            break
        else:
            print('invalid answer "%s"!' % confirm)
            print('JUST enter "Y" or "N"...')
    return root


def find_and_add_svn_dir_to_global_list(project_root: str) -> None:
    print('walking through project root "%s"...' % project_root)
    for root, dirs, files in os.walk(project_root):
        if platform_is_windows:
            relative_root_list = root.split("\\")
        else:
            relative_root_list = root.split("/")
        root_name = relative_root_list[-1]
        if root_name == ".svn" or root_name == "build":
            global_svn_dir_list.append(root)


def removing_directory(path: str) -> None:
    if platform_is_windows:
        os.system('DEL /S /F /Q "%s" 1>nul' % path)
        os.system('RMDIR /S /Q "%s" 1>nul' % path)
    else:
        os.system('rm -rf "%s"' % path)


def del_all_svn_dir_from_global_list() -> None:
    for path in global_svn_dir_list:
        removing_directory(path)
        print("removing dir: %s" % path)


def main(argv: list) -> None:
    project_root = read_root_config_from_argv(argv)
    project_root = let_user_confirm_the_root(project_root)
    find_and_add_svn_dir_to_global_list(project_root)
    del_all_svn_dir_from_global_list()


if __name__ == '__main__':
    detect_platform()
    main(sys.argv[1:])
