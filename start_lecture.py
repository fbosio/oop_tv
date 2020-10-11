#!/usr/bin/env python3
import subprocess
import sys
from PyQt5.QtGui import QGuiApplication, QImage


app = QGuiApplication([])
geometry = app.primaryScreen().availableGeometry()

image = QImage('img/tvfg.png')
ratio = image.height() / image.width()

names = 'be_in_my_video', 'i_am_the_slime'
N = len(names)

if geometry.height() >= geometry.width() * ratio:
    width = geometry.width() / (N*ratio)
    x = geometry.width() - geometry.height()/(N*ratio)
else:
    width = geometry.width() / N
    x = geometry.width() / N
height = width*ratio
y = geometry.height() + ratio*(x-geometry.width())

for i, name in enumerate(names):
    subprocess.Popen([sys.executable, 'main.py', '-n', name, '-g',
                     f'{i*x}', f'{i*y}', f'{width}', f'{height}'])
