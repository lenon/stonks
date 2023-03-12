class PositionNotOpenError(Exception):
    def __init__(self, symbol: str):
        super().__init__(f"position not open: {symbol}")


class UnknownEventError(Exception):
    def __init__(self, event: str):
        super().__init__(f"unknown event type: {event}")
