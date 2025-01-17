import os
from pathlib import Path


def create_file(file_path, file_name, file_content):
    file_path = Path(file_path)  # Convert file_path to a Path object
    if not os.path.exists(file_path):
        os.makedirs(file_path, exist_ok=True)
        print(f"Directory {file_path} created")
    with open(file_path.joinpath(file_name), "w") as f:
        f.write(file_content)
        print(f"File {file_name} created")


# create_file(
#     ("autoUtils/henry33/"),
#     "abc.py",
#     "111",
# )
