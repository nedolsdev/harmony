"""Volume helpers."""


def check_volume(volume: float) -> None:
    """Raise error if volume is out of range."""
    if volume < 0 or volume > 1:
        msg = "Volume should be in range between 0 and 1."
        raise ValueError(msg)
