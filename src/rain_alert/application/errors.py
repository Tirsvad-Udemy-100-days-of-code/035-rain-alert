"""Errors raised through the ports of the application layer."""


class ForecastUnavailableError(Exception):
    """@brief Raised when the forecast source cannot give a usable forecast."""
