import logging
import os
import argparse
import time
import hashlib
import sys
from datetime import datetime

def setup_logging():
    """
    Configure logging for the application.
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

def sha256_checksum(file_path):
    """
    Compute the SHA-256 checksum of a file.
    """
    try:
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return file_hash.hexdigest()
    except Exception as e:
        logging.error(f"Error computing checksum for {file_path}: {e}")
        return None

def read_command_line_args():
    """
    Read arguments from the command line.
    """
    parser = argparse.ArgumentParser(description='One-way folder synchronization.')
    parser.add_argument('source', type=str, help='Source directory')
    parser.add_argument('replica', type=str, help='Replica directory')
    parser.add_argument('interval', type=int, help='Synchronization interval (seconds)')
    args = parser.parse_args()

    logging.info(f"Source directory: {args.source}")
    logging.info(f"Replica directory: {args.replica}")
    logging.info(f"Sync interval: {args.interval} seconds")
    return args.source, args.replica, args.interval

def ensure_directories_exist(source_dir, replica_dir):
    """
    Ensure that the source directory exists and create the replica directory if needed.
    """
    if not os.path.exists(source_dir):
        logging.error(f"Source directory does not exist: {source_dir}")
        sys.exit(1)

    if not os.path.exists(replica_dir):
        os.makedirs(replica_dir)
        logging.info(f"Created missing replica directory: {replica_dir}")

def sync_folders(source_dir, replica_dir):
    """
    Synchronize the source folder with the replica folder.
    """
    logging.info("Starting synchronization...")

    source_files = set()
    replica_files = set()

    # Walk through source directory
    for root, _, files in os.walk(source_dir):
        rel_path = os.path.relpath(root, source_dir)
        for file in files:
            source_files.add(os.path.join(rel_path, file))

    # Walk through replica directory
    for root, _, files in os.walk(replica_dir):
        rel_path = os.path.relpath(root, replica_dir)
        for file in files:
            replica_files.add(os.path.join(rel_path, file))

    # Remove files that shouldn't be in replica
    for file in replica_files - source_files:
        file_path = os.path.join(replica_dir, file)
        try:
            os.remove(file_path)
            logging.info(f"Removed: {file_path}")
        except Exception as e:
            logging.error(f"Error removing {file_path}: {e}")

    # Copy/update files from source to replica
    for file in source_files:
        source_path = os.path.join(source_dir, file)
        replica_path = os.path.join(replica_dir, file)

        os.makedirs(os.path.dirname(replica_path), exist_ok=True)

        try:
            if not os.path.exists(replica_path) or sha256_checksum(source_path) != sha256_checksum(replica_path):
                with open(source_path, 'rb') as src, open(replica_path, 'wb') as dst:
                    dst.write(src.read())
                logging.info(f"Copied/Updated: {replica_path}")
        except Exception as e:
            logging.error(f"Error copying {source_path} to {replica_path}: {e}")

    logging.info("Synchronization completed.")

def main():
    """
    Main function for running the synchronization process.
    """
    setup_logging()
    source_dir, replica_dir, interval = read_command_line_args()
    ensure_directories_exist(source_dir, replica_dir)

    try:
        while True:
            sync_folders(source_dir, replica_dir)
            time.sleep(interval)
    except KeyboardInterrupt:
        logging.info("Synchronization stopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()

