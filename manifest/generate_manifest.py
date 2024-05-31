"""
Example usage

- Put your CSV files under a folder named "C:/Desktop/data_feed"
- Set the value of FOLDER_PATH variable (generate_manifest.py file, 6th line) as "C:/Desktop/data_feed"
- Run the generate_manifest.py script with python3 using this command: "python3 generate_manifest.py"
- This script generates a file called "manifest" in the same folder with the CSV files.
"""
import os
import hashlib

### Parameter: FOLDER_PATH
### This should be a directory with CSV files in it. Example: "/home/data"
FOLDER_PATH: str = ""


def hash_local_file(file_path, chunk_size):
    print(f"calculating checksum of {file_path} file")
    sha1 = hashlib.sha1()
    with open(file_path, mode="rb") as buffered_reader:
        chunk = buffered_reader.read(chunk_size)
        while chunk:
            sha1.update(chunk)
            chunk = buffered_reader.read(chunk_size)
    hash_result = sha1.hexdigest()
    print(f"checksum result: {hash_result}")
    return hash_result


def get_checksum(folder_path, file_names, chunk_size):
    print(f"calculating checksum of files in the {folder_path}")
    print(f"files: {file_names}")
    # create {file_name: checksum} mapping/dictionary
    checksum = {}
    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)
        file_checksum = hash_local_file(
            file_path=file_path,
            chunk_size=chunk_size,
        )
        checksum[file_name] = file_checksum
    print("calculated checksum results: ")
    print(sorted(checksum.items()))
    return checksum


def prepare_manifest_content(checksum: dict, delimiter: str) -> str:
    hash_algorithm = "SHA1"
    manifest = ""
    for file_name, sha1 in sorted(checksum.items()):
        manifest += f"{file_name}{delimiter}{hash_algorithm}{delimiter}{sha1}\n"
    return manifest


def generate(folder_path):
    # ensure that folder_path ends with "/" character
    if not folder_path.endswith("/"):
        folder_path += "/"
    # get files and directories in the directory
    _, _, file_names = next(os.walk(folder_path))
    # if a manifest file already exists in the directory,
    # remove it from the file list
    if "manifest" in file_names:
        print("manifest file already exists")
        file_names.remove("manifest")
    # calculate checksums
    checksum = get_checksum(
        folder_path=folder_path,
        file_names=file_names,
        chunk_size=10,
    )
    # generate manifest file content
    manifest = prepare_manifest_content(checksum=checksum, delimiter=" ")
    manifest_file_path = os.path.join(folder_path, "manifest")
    # if the manifest file already exists, overwrite it, otherwise create it.
    with open(manifest_file_path, "w", encoding="utf-8") as manifest_file:
        manifest_file.write(manifest)


if __name__ == "__main__":
    generate(FOLDER_PATH)
