import webbrowser
from zipfile import ZipFile
import os
import subprocess
import sys
import time


def zip_files(zip_file_name, file_paths):
    if ".zip" != zip_file_name[-4:]:
        zip_file_name += ".zip"

    try:
        with ZipFile(zip_file_name, 'w') as zipping:
            for file in file_paths:
                zipping.write(file)
    except Exception as e:
        print("------- Exception while zipping !\n\n\n")
        raise e


def open_drive():
    url = r'https://drive.google.com/drive/my-drive'
    chrome_app = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s --incognito'
    if os.path.isfile(chrome_app):
        webbrowser.get(chrome_path).open_new(url)
    else:
        webbrowser.open_new(url)


def save_to_drive():
    dirname = "ZipBackup"
    original_path = os.getcwd()

    files = os.listdir()
    zipping = []
    for file in files:
        if file[-4:] == ".SDE":
            zipping.append(file)

    try:
        os.makedirs(dirname)
    except:
        pass

    try:
        zip_files(os.path.join(dirname, "SDE-Backup.zip"), zipping)
    except Exception as e:
        print("Unable to zip files properly")
        print(e)
    try:
        open_drive()
    except Exception as e:
        print("Unable to open drive properly")
        print(e)
    time.sleep(1)
    open_file(os.path.join(original_path, dirname))


def open_file(filename):
    try:
        os.startfile(filename)
    except Exception as e:
        print("No folder in path 1 of opening")
        try:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])
        except:
            print("Not able to open folder using path 2!")
