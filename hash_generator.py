import argparse
import os
import sys

from blake3 import blake3


def parse_args():
    """
        Function to parse required arguments.
    """
    parser = argparse.ArgumentParser(description='Generate the BLAKE3 hash.')
    parser.add_argument('-f', '--file')
    args = parser.parse_args()
    return args


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


def generate_blake3_hashes(directory_path):
    """
    Generate BLAKE3 hashes for all files in a given directory.

    Args:
        directory_path (str): Path to the directory.

    Returns:
        dict: A dictionary containing file names as keys and their corresponding BLAKE3 hashes as values.
    """
    file_hashes = {}
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_hashes[file_name] = generate_blake3_hash(file_path)
    return file_hashes


def main(file_path):
    """
        Main function
    """
    if os.path.isfile(file_path):
        print(f"BLAKE3 hash of '{file_path}': {generate_blake3_hash(file_path).hex()}")
    elif os.path.isdir(file_path):
        hashes = generate_blake3_hashes(file_path)
        print(f"BLAKE3 hashes for files in the directory '{file_path}':")
        for filename, hash_val in hashes.items():
            print(f"{filename}: {hash_val.hex()}")
    else:
        print(f"Invalid file or directory path: '{file_path}'.")
        sys.exit(1)


if __name__ == '__main__':
    inputs = parse_args()
    main(inputs.file)
