class TV:
    """A television."""
    def __init__(self):
        self._on = False
        self._channel = 0
        self._channels = 4

    def power(self):
        """Toggle between `on' and `off' states."""
        self._on = not self._on

    def is_on(self):
        """Return True when `on', False otherwise."""
        return self._on

    def channel_up(self):
        if self._on:
            self._channel += 1
            self._channel %= self._channels

    def channel_down(self):
        if self._on:
            self._channel -= 1
            self._channel %= self._channels

    def channel(self):
        """Return the current channel number, if `on'."""
        if self._on:
            return self._channel
