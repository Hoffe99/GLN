import os
import shutil

# Destination directory
destination_directory = "/path/to/destination/directory"

# Source directory
source_directory = "/path/to/source/directory"

# List of files to copy
files_to_copy = ["file1.txt", "file2.txt", "file3.txt"]

# Copy files
for file in files_to_copy:
    source = os.path.join(source_directory, file)
    destination = os.path.join(destination_directory, file)
    shutil.copy2(source, destination)
    print(f"File {file} copied from {source} to {destination}")