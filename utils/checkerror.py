import logging



LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(
    level=logging.DEBUG,
    format=LOG_FORMAT,
)

logger = logging.getLogger()

def log_error(err):
    global logger
    if err is not None:
        logger.error(err)
        return False


def log_debug(err):
    global logger
    if err is not None:
        logger.info(err)
        return True


if __name__ == '__main__':
    log_error('TEST:Something went wrong')
