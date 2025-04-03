import logging
import os
import argparse
import time
from datetime import datetime

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





def read_the_arguments_from_command_line(logger):
    """
    Read the arguments from the command line
    """

    parser = argparse.ArgumentParser(description='Synchronize directories')
    parser.add_argument('source', type=str, nargs='?', help='Source directory')
    parser.add_argument('replica', type=str, nargs='?', help='Replica directory')
    parser.add_argument('interval', type=int, nargs='?', help='Interval in seconds')
    args = parser.parse_args()

    logger.info(f"Source directory: {args.source}")
    logger.info(f"Replica directory: {args.replica}")
    logger.info(f"Interval: {args.interval}")
    return args.source, args.replica, args.interval



def check_the_folders_exist(source_dir, replica_dir, logger):

    """
    Check if the source and replica directories exist
    """

    if not os.path.exists(source_dir):
        logger.error(f"Source directory does not exist: {source_dir}")
        return False
    if not os.path.exists(replica_dir):
        logger.error(f"Replica directory does not exist: {replica_dir}")
        os.makedirs(replica_dir)
        logger.info(f"Created replica directory: {replica_dir}")
        return False
    return True







def sync_directories(source_dir, replica_dir , interval, logger):

    """
    One way folder syncrenization from source to replica folders periodically
    """
    logger.info(f"Synchronizing directories at {datetime.now()}")
    time.sleep(interval)
    logger.info(f"Synchronization completed at {datetime.now()}")



def main():
    """
    main function for the application
    """
    setup_logging()
    source_dir, replica_dir, interval = read_the_arguments_from_command_line(logging)
    check_the_folders_exist(source_dir, replica_dir, logging)
    sync_directories(source_dir, replica_dir, interval, logging)




if __name__ == "__main__":
    main()
