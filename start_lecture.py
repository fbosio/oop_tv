#!/usr/bin/env python3
import subprocess
import sys
from PyQt5.QtGui import QGuiApplication, QImage


app = QGuiApplication([])
geometry = app.primaryScreen().availableGeometry()

image = QImage('img/tvfg.png')
ratio = image.width() / image.height()

names = 'be_in_my_video', 'i_am_the_slime', 'the_radio_is_broken'

width = min(min(geometry.width(), geometry.height() * ratio),
            max(geometry.width(), geometry.height() * ratio) / len(names))
height = width / ratio

for i, name in enumerate(names):
    x = y = 0
    if geometry.width() >= geometry.height() * ratio:
        x = i * min(geometry.width()/len(names), geometry.height()*ratio)
    else:
        y = i * min(geometry.width()/ratio, geometry.height()/len(names))
    print(x, y)
    subprocess.Popen([sys.executable, 'main.py', '-n', name, '-g',
                     f'{x}', f'{y}', f'{width}', f'{height}'])
