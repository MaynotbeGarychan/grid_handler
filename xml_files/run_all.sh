#!/bin/bash

# Set the project directory
project_dir="$1"

# Check if the project directory is provided
if [ -z "$project_dir" ]; then
    echo "Usage: $0 <project_directory>"
    exit 1
fi

# Find all subdirectories containing run.sh
subfolders=$(find "$project_dir" -type d -name "*run.sh" -exec dirname {} \;)

# Iterate through each subfolder and run the run.sh script
for folder in $subfolders; do
    echo "Running $folder/run.sh"
    (cd "$folder" && ./run.sh)
done

echo "All run.sh scripts executed successfully."
