import os
import shutil
import random
from datetime import datetime
import pathlib

noConsoleLauncher = True
noConsoleGame = True

def buildMainGame():
    print("building main game")
    os.system(f"pyinstaller --noconfirm --add-data=assets:assets {"--noconsole" if noConsoleGame else ""} --icon=assets/images/icon.ico main.py")

def buildLauncher():
    print("building launcher")
    os.chdir("installer")
    os.system(f"pyinstaller {"--noconsole" if noConsoleLauncher else ""} --onefile --icon=icon.ico launcher.py")
    
def buildInstaller():
    print("building installer")
    if not os.getcwd().endswith("installer"):
        os.chdir("installer")
    os.system(f"pyinstaller {"--noconsole" if noConsoleLauncher else ""} --onefile --icon=icon.ico installer.py")

def copyFiles():
    if os.getcwd().endswith("installer"):
        os.chdir("..")
    os.chdir("dist")
    
    rootdir = pathlib.Path(os.getcwd()).parent
    
    print(rootdir)
    version = input("version: ")
    
    name = f"CreateTheSun-{version}-{datetime.now().strftime('%m-%d-%Y')}-{hex(round(random.random() * 10000))}"
    os.mkdir(name)
    
    os.chdir(name)
    buildDir = os.getcwd()

    print("copying files")
    
    # no need for this anymore lol shutil.copytree(os.path.join(rootdir, "assets"), os.path.join("assets"))
    
    shutil.copytree(os.path.join(rootdir, "dist", "main"), buildDir, dirs_exist_ok=True)
    
    #shutil.copy(os.path.join(rootdir, "installer", "dist", "launcher.exe"), buildDir)
    
    print("done copying files")
    print("zipping files")
    os.chdir("..")
    shutil.make_archive(name, "zip", name)
    print("done zipping files, filename is " + f"{name}.zip")    

def build():
    print("DID YOU REMEMBER TO: \n test all features\nCheck if all gamedefine values are set to the base amount\nEnsure that quickLaunch is set to False")
    input("Press enter to continue")
    buildMainGame()
    buildLauncher()
    buildInstaller()
    copyFiles()
    input("Build complete, press enter to exit (installer is located in launcher/dist/installer.exe))")

if __name__ == "__main__":
    build()
else:
    print("this is a script, not a module")
