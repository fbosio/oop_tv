from PyQt5.QtCore import QCoreApplication, QPoint, QRect, QRectF, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor

from tv import TV
from buttons import Panel
from display import ChannelNumber


class OopTv(QWidget):
    """Application window class. Paint cute things on the screen.

    Input:
        `names`: sequence of image names (str)
        `pixmaps`: sequence of corresponding QPixmap objects
        `debug`: whether the app prints text in console or not
    """
    def __init__(self, names, pixmaps, options):
        super().__init__(windowTitle=options['title'])
        geometry = options['geometry']
        if geometry is not None:
            self.setGeometry(QRect(*geometry))

        debug = options['debug']
        self.pixmaps = dict(zip(names, pixmaps))
        self.tv = TV()
        self.panel = Panel(self, self.tv, debug)

        # Order pixmaps according to channels
        self._contents = pixmaps[1:]

        # Display channel number
        self.channel_number = ChannelNumber(self, self.tv, debug)

        if debug:
            print('Loaded.')
            print('You can click on the screen to get the mouse position.')
            print('Position `x` is expressed as a percentage of the window '
                  'width,')
            print(' `y` is expressed as a percentage of the height.')
        self.debug = debug

    def paintEvent(self, event):
        """Paint cute things, internal use."""
        # override QWidget.paintEvent
        w, h = self.width(), self.height()

        # The following values were obtained by mouse tracking
        screen = QRectF(0.12 * w, 0.1 * h, 0.74 * w, 0.71 * h)
        led_position = QPoint(0.625 * w, 0.913 * h)

        # Paint screen
        qp = QPainter()
        qp.begin(self)
        self._paint(screen, qp)
        self.channel_number.paint(qp)
        pixmap = self.pixmaps['tvfg.png']
        qp.drawPixmap(QRect(0, 0, w, h), pixmap,
                      QRect(0, 0, pixmap.width(), pixmap.height()))
        self._glow(led_position, qp)
        self.panel.paint(qp)
        qp.end()

    def _paint(self, screen, qp):
        """Paint TV screen.

        Subroutine, internal use.
        """
        if self.tv.is_on():
            pixmap = self._contents[self.tv.channel()]
            qp.drawPixmap(screen, pixmap,
                          QRectF(0, 0, pixmap.width(), pixmap.height()))
        else:
            qp.fillRect(screen, Qt.black)

    def _glow(self, point, qp):
        """Paint TV led.

        Subroutine, internal use.
        """
        if self.tv.is_on():
            pen = qp.pen()
            brush = qp.brush()

            qp.setPen(Qt.transparent)

            # light diffusion
            radius = 5
            qp.setBrush(QBrush(QColor(0, 255, 0, 20)))
            qp.drawEllipse(point, radius, radius)

            # light per se
            radius = 1
            qp.setBrush(QBrush(Qt.green))
            qp.drawEllipse(point, radius, radius)

            # reset
            qp.setPen(pen)
            qp.setBrush(brush)

    def mousePressEvent(self, event):
        """Does stuff when clicked, internal use."""
        x, y = event.x(), event.y()
        self.panel.event(x, y)

        # buttons() method gives a flag, which should be filtered by bitmasking
        if self.debug and event.buttons() & Qt.LeftButton:
            print(f'Clicked at ({100 * x / self.width():.4f}% of width, '
                  f'{100 * y / self.height():.4f}% of height)')


def run(options):
    """Run the app with the given `options`.

     `options` should be a dict with some of the following keys:
         'debug' (bool): wheter or not the app shows things in the console
         'geometry' (list): four ints that specifies x, y, width and height of
            the window.
         'title' (str): window title.
    """
    # IPython compatibility
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication([])

    # Load images, if possible
    folder = 'img/'
    names = ('tvfg.png', 'white_noise.jpg', 'guido.png', 'ricky.jpg',
             'johnny.jpg')
    pixmaps = []

    for name in names:
        pixmaps.append(QPixmap(folder + name))

    window = OopTv(names, pixmaps, options)

    for pixmap, name in zip(pixmaps, names):
        if pixmap.isNull():
            QMessageBox.critical(window, 'Error fatal',
                                 f'No se encontró {folder+name}')
            break
    else:
        # Run the app after load all files
        window.show()
        app.exec_()
