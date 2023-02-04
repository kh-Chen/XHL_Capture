# XHL_Capture
某直播平台录播工具整合工程


* win版窗口化工具
>入口文件：main.py  
>使用方式请自行摸索。

* linux版自动化录播工具
>入口文件：xhlCRS.py  
>定时启动需手动配置crontab任务

注意事项
* 两个工具需要在各自合适的环境下编译。
* 当前仓库中的venv虚拟环境是win版用的，linux版需重新创建虚拟环境并安装依赖库。
* 配置文件为config.ini，请自行填写相应的值。
* 本程序某些模式由于已经长时间弃用，不保证可靠性。

| package                   | version    | package                   | version    |
|---------------------------|------------|---------------------------|------------|
| Brotli                    | 1.0.9      | pefile                    | 2021.9.3   |
| JPype1                    | 1.3.0      | pip                       | 22.0.4     |
| PyNaCl                    | 1.5.0      | psutil                    | 5.9.0      |
| PyQt5                     | 5.15.4     | ptyprocess                | 0.7.0      |
| PyQt5-Qt5                 | 5.15.2     | pycparser                 | 2.21       |
| PyQt5-sip                 | 12.9.1     | pyinstaller               | 4.10       |
| PyQt5-stubs               | 5.15.2.0   | pyinstaller-hooks-contrib | 2022.2     |
| altgraph                  | 0.17.2     | pyqt5-plugins             | 5.15.4.2.2 |
| bcrypt                    | 3.2.0      | pyqt5-tools               | 5.15.4.3.2 |
| certifi                   | 2021.10.8  | python-dotenv             | 0.19.2     |
| cffi                      | 1.15.0     | python-vlc                | 3.0.16120  |
| charset-normalizer        | 2.0.12     | pywin32-ctypes            | 0.2.0      |
| click                     | 7.1.2      | qt5-applications          | 5.15.2.2.2 |
| cryptography              | 36.0.2     | qt5-tools                 | 5.15.2.1.2 |
| future                    | 0.18.2     | requests                  | 2.27.1     |
| idna                      | 3.3        | setuptools                | 60.10.0    |
| logger                    | 1.4        | six                       | 1.16.0     |
| paramiko                  | 2.10.3     | urllib3                   | 1.26.9     |

















