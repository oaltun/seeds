from datetime import datetime
import logging


def loggers_get():

    # Get current datetime
    now = datetime.now()

    # Format datetime to string
    formatted_now = now.strftime("%Y_%m_%d_%H_%M_%S")

    # Create a logger for detailed logs
    detailed_logger = logging.getLogger("DetailedLogger")
    detailed_logger.setLevel(logging.DEBUG)
    detailed_fh = logging.FileHandler(f"logs/detailed.{formatted_now}.log")
    detailed_formatter = logging.Formatter('---- %(asctime)s - %(name)s - %(levelname)s - %(message)s')
    detailed_fh.setFormatter(detailed_formatter)
    detailed_logger.addHandler(detailed_fh)

    # Create another logger for summary logs
    summary_logger = logging.getLogger("SummaryLogger")
    summary_logger.setLevel(logging.DEBUG)
    summary_fh = logging.FileHandler(f"logs/summary.{formatted_now}.log")
    summary_formatter = logging.Formatter('---- %(asctime)s - %(message)s')
    summary_fh.setFormatter(summary_formatter)
    summary_logger.addHandler(summary_fh)

    return detailed_logger, summary_logger
