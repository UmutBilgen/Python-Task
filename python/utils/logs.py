import logging

def get_logging():
    """
    Configure and retrieve a logger instance for logging messages.

    Returns:
    logging.Logger: A configured logger instance.

    The logger is configured to write log messages to a file ('logs/logs.log').
    The logging level is set to DEBUG, allowing all log messages to be recorded.
    The log message format includes the timestamp, log level, and the message itself.
    """
    logging.basicConfig(
        filename='logs/logs.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)
