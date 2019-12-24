import logging


LOGGER = logging.getLogger("transport_task")
LOGGER.setLevel(logging.INFO)
fh = logging.FileHandler("transport_task.log")
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
LOGGER.addHandler(fh)
