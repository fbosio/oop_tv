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
x = y = 0

for i, name in enumerate(names):
    if geometry.width() >= geometry.height() * ratio:
        x = i * min(geometry.width()/len(names), geometry.height()*ratio)
        y = i * geometry.height() / len(names)
    else:
        x = i * geometry.width() / len(names)
        y = i * min(geometry.width()/ratio, geometry.height()/len(names))
    subprocess.Popen([sys.executable, 'main.py', '-n', name, '-g',
                     f'{x}', f'{y}', f'{width}', f'{height}'])
