#!/bin/bash

# Function to create folders and files recursively
create_structure() {
  local source_path=$1
  local destination_path=$2

  # Create the folder with "test_" prefix
  mkdir -p "${destination_path}/test_$(basename ${source_path})"

  # Loop through files and subdirectories
  for item in "${source_path}"/*; do
    if [[ -d "${item}" && "$(basename ${item})" != "__pycache__" ]]; then
      # Recursively create subdirectories
      create_structure "${item}" "${destination_path}/test_$(basename ${source_path})"
    elif [[ -f "${item}" && "$(basename ${item})" != "__init__.pyc" ]]; then
      # Copy and rename files with "test_" prefix
      cp "${item}" "${destination_path}/test_$(basename ${source_path})/test_$(basename ${item})"
    fi
  done
}

# Set the source and destination paths
source_path="api"
destination_path="test_api"

# Create the structure
create_structure "${source_path}" "${destination_path}"

echo "Folder structure with 'test_' prefix created in ${destination_path}"
