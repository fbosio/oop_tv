from PyQt5.QtCore import QRectF, QRect, QPoint
from PyQt5.QtGui import QColor


class Panel:
    """TV Button Panel.

    Call the `paint` method on a QWidget.paintEvent.
    Call the `event` method on a QWidget.mousePressEvent.

        `window`: the QWidget
        `tv`: the TV object
        `debug`: a bool to show or hide information in the development stage.
    """
    def __init__(self, window, tv, debug):
        self.window = window
        self.tv = tv
        self.debug = debug

        # Boundaries (fractions of width and height of the screen)
        self.top = 0.87
        self.left = 0.399
        self.bottom = 0.93
        self.right = 0.73

        # Little buttons
        width = 0.0375
        height = self.bottom - self.top
        self.buttons = []

        for i in range(5):
            x = self.left + i*width
            rect = QRectF(x, self.top, width, height)
            self.buttons.append(Button(rect))

        # Big button (power)
        left = 0.66
        width = self.right - left
        rect = QRectF(left, self.top, width, height)
        self.buttons.append(Button(rect))

        # Buttons callbacks
        self._bind_callbacks()

    def paint(self, qp):
        """Show panel and buttons as coloured rectangles if `debug` is True."""
        if self.debug:
            w, h = self.window.width(), self.window.height()
            rect = QRect(QPoint(self.left * w, self.top * h),
                         QPoint(self.right * w, self.bottom * h))

            qp.fillRect(rect, QColor(0, 0, 255, 128))
            qp.setPen(QColor(0, 255, 255))

            for button in self.buttons:
                qp.drawRect(button.absolute_bounds(w, h))

    def event(self, x, y):
        """Trigger button events when clicked."""
        w, h = self.window.width(), self.window.height()
        for button in self.buttons:
            button.event(x, y, w, h)

    def _bind_callbacks(self):
        def channel_up():
            self.tv.channel_up()
            self.window.update()

        def channel_down():
            self.tv.channel_down()
            self.window.update()

        def big_button_callback():
            self.tv.power()
            self.window.update()

        self.buttons[3].bind(channel_up)
        self.buttons[4].bind(channel_down)

        self.buttons[-1].bind(big_button_callback)


class Button:
    def __init__(self, rectangle):
        self.x = rectangle.x()
        self.y = rectangle.y()
        self.width = rectangle.width()
        self.height = rectangle.height()

        def default_callback():
            pass

        self._callback = default_callback

    def absolute_bounds(self, w, h):
        return QRect(self.x * w, self.y * h, self.width * w, self.height * h)

    def event(self, x, y, w, h):
        bounds = self.absolute_bounds(w, h)
        if bounds.contains(x, y, False):
            self._callback()

    def bind(self, callback):
        self._callback = callback
