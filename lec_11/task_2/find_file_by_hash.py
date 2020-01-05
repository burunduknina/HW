import hashlib
import os

import fire


def calc_hash(path):
    with open(path, "rb") as f:
        content = f.read()
        return hashlib.sha256(content).hexdigest();


def get_files_by_hash(path, sha_hash):
    files = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if calc_hash(file_path) == sha_hash:
                files.append(file_path)
    return files


if __name__ == '__main__':
    fire.Fire(get_files_by_hash)
