from PyQt5.QtCore import QRectF, QPoint, Qt, QTimer


class ChannelNumber:
    """Channel number to display.

    Call the `paint` method on a QWidget.paintEvent.

    The `hide` method is used by an internal timer.
    It may be called to hide the channel number though.
    """
    def __init__(self, window, tv, debug):
        self.window = window
        self.tv = tv
        self.debug = debug

        # Boundaries (fractions of width and height of the screen)
        self.top = 0.18
        self.left = 0.64
        self.bottom = 0.3
        self.right = 0.8

        # Text disappears after certain time
        self.visible = False
        self._was_on = False
        self._prev_channel = None
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide)

    def paint(self, qp):
        """Display channel number on TV."""
        channel = self.tv.channel()

        if self.tv.is_on():
            if not self._was_on:
                self.show()
                self._was_on = True

            if self.visible:
                w, h = self.window.width(), self.window.height()
                rect = QRectF(QPoint(self.left * w, self.top * h),
                              QPoint(self.right * w, self.bottom * h))

                if channel == 0:
                    text = 'AV'
                else:
                    text = str(channel)

                scale_factor = rect.height() / qp.fontMetrics().height()
                font = qp.font()
                font.setPointSizeF(font.pointSizeF() * scale_factor)
                qp.setFont(font)
                qp.setPen(Qt.green)
                qp.drawText(rect, Qt.AlignRight | Qt.AlignVCenter, text)

            if self._prev_channel != channel:
                self.show()
                self.window.update()
                self._prev_channel = channel
        else:
            self._was_on = False

    def show(self):
        """Activate channel number displaying."""
        self.visible = True
        self.timer.start(2000)

    def hide(self):
        """Timer callback."""
        self.visible = False
        self.window.update()
