import logging


def setup_logging():
    """
    logging configuration for the application
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_format = '%(asctime)s ::: %(levelname)s ::: %(message)s'
    formatter = logging.Formatter(log_format)

    file_handler = logging.FileHandler('sync.log', mode='w')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

def main():
    """
    main function for the application
    """
    setup_logging()

    logging.info('Starting the synchronization process')
    source_dir = 'source_dir'
    replica_dir = 'replica_dir'
    logging.info(f'Using source directory: {source_dir}')
    logging.info(f'Using replica directory: {replica_dir}')

if __name__ == "__main__":
    main()
