import argparse
import hashlib
import logging
import os
import sys

from blake3 import blake3


def parse_args():
    """
        Function to parse required arguments.
    """
    parser = argparse.ArgumentParser(description='Generate the hashes of a given file path.')
    parser.add_argument('-f', '--file')
    parser.add_argument('-l', '--log', default='hashes.txt')
    args = parser.parse_args()
    return args


def generate_sha256_hash(file_path):
    """
    Generate the SHA-256 hash for a given file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: The SHA-256 hash of the file.
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def generate_blake3_hash(file_path):
    """
    Generate the BLAKE3 hash for a given file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: The BLAKE3 hash of the file.
    """
    hasher = blake3()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.digest()


def generate_hashes(directory_path):
    """
    Generate SHA-256 and BLAKE3 hashes for all files in a given directory.

    Args:
        directory_path (str): Path to the directory.

    Returns:
        dict: A dictionary containing file names as keys and their corresponding SHA-256 and BLAKE3 hashes as values.
    """
    file_hashes = {}
    for root, _, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            sha256_hash = generate_sha256_hash(file_path)
            blake3_hash = generate_blake3_hash(file_path)
            file_hashes[filename] = {'SHA-256': sha256_hash, 'BLAKE3': blake3_hash.hex()}
    return file_hashes


def setup_logging(log_file):
    """
        Define logging behavior.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[
            logging.FileHandler(log_file, mode='a'),
            logging.StreamHandler()
        ]
    )


def log_hash(filename, sha256_hash, blake3_hash):
    """
        Log hashes of the file.
    """
    logging.info("%s:", filename)
    logging.info("    SHA-256: %s", sha256_hash)
    logging.info("    BLAKE3: %s", blake3_hash)


def main(file_path, log_path):
    """
        Main function
    """
    setup_logging(log_path)
    
    if os.path.isfile(file_path):
        log_hash(file_path, generate_sha256_hash(file_path), generate_blake3_hash(file_path).hex())
    elif os.path.isdir(file_path):
        hashes = generate_hashes(file_path)
        print(f"Hashes for files in the directory '{file_path}':")
        for filename, hash_values in hashes.items():
            log_hash(filename, hash_values['SHA-256'], hash_values['BLAKE3'])
    else:
        print(f"Invalid file or directory path: '{file_path}'.")
        sys.exit(1)


if __name__ == '__main__':
    inputs = parse_args()
    main(inputs.file, inputs.log)
