#!/usr/bin/python3
import os
import sys
import subprocess
shortcut_content_templ = """
[Desktop Entry]
Encoding=UTF-8
Name={name}
Comment=null
Exec={exec}
Icon={icon}
Terminal=false  
StartupNotify=false
Type=Application
Categories=Application
"""
def get_desktop_path():
    user_home_path = os.environ['HOME']
    path = user_home_path + "/Desktop"
    return path if os.path.exists(path) else user_home_path + "/桌面"

def verify_path(paths):
    for path in paths:
        if not os.path.exists(path):
            print(f"path:{path} is not exist")
            exit(0)

def get_shell_path():
    x = subprocess.Popen("pwd",stdout=subprocess.PIPE)
    return x.stdout.readlines()[0].decode('utf-8')

def to_absolut_path(path):
    shell_path = get_shell_path().strip("\n")
    return shell_path + "/" + path 

if __name__ == "__main__":
   
    exec = sys.argv[1]
    icon = sys.argv[2] if len(sys.argv)==3 else "icon/icon.png"
    desktop_path = get_desktop_path()
    verify_path([exec,icon,desktop_path])
    path_with_name = f"{desktop_path}/{exec}.desktop"
    with open(path_with_name,'w') as file:
        shortcut_content = shortcut_content_templ.format(name = exec,exec=to_absolut_path(exec),icon=to_absolut_path(icon))
        file.write(shortcut_content)
    