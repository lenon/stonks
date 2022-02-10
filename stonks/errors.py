class PositionNotOpenError(Exception):
    def __init__(self, symbol):
        super().__init__(f"position not open: {symbol}")


class UnknownEventError(Exception):
    def __init__(self, event):
        super().__init__(f"unknown event type: {event}")
