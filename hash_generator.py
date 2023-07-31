import argparse
import hashlib
import os
import sys

from blake3 import blake3


def parse_args():
    """
        Function to parse required arguments.
    """
    parser = argparse.ArgumentParser(description='Generate the hashes of a given file path.')
    parser.add_argument('-f', '--file')
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


def main(file_path):
    """
        Main function
    """
    if os.path.isfile(file_path):
        print(f"    {file_path}:")
        print(f"        SHA-256: {generate_sha256_hash(file_path)}")
        print(f"        BLAKE3: {generate_blake3_hash(file_path).hex()}")
    elif os.path.isdir(file_path):
        hashes = generate_hashes(file_path)
        print(f"Hashes for files in the directory '{file_path}':")
        for filename, hash_values in hashes.items():
            print(f"    {filename}:")
            print(f"        SHA-256: {hash_values['SHA-256']}")
            print(f"        BLAKE3: {hash_values['BLAKE3']}")
    else:
        print(f"Invalid file or directory path: '{file_path}'.")
        sys.exit(1)


if __name__ == '__main__':
    inputs = parse_args()
    main(inputs.file)
