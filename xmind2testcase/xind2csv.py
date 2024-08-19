# coding:utf-8
import subprocess
import os


def run_cmd_command():
    # command = 'pyinstaller -F cli.py -n xmind2csv_F --add-data="../webtool;webtool"'
    command = 'pyinstaller --onefile -n xmind2csv --add-data="../webtool;webtool" cli.py'
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    # 确保工作目录正确
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_cmd_command()
    # 你的其他代码
