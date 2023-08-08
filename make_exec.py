import subprocess


if __name__ == "__main__":
    subprocess.call(["pyinstaller", "--onefile", "main.py"])
