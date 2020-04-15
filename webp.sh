#!/bin/bash

find . -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) -print0 | while IFS= read -r -d $'\0' file; do
  # Get the directory of the original file
  file_dir=$(dirname "$file")

  # Extract the filename without the extension
  filename=$(basename "$file")
  extension="${filename##*.}"
  name_without_ext="${filename%.*}"

  # Construct the output filename with the correct directory
  output_file="${file_dir}/${name_without_ext}.webp"

  # Execute cwebp
  echo "Converting '$file' to '$output_file'..."
  cwebp -q 78 -m 5 -preset picture -metadata none "$file" -o "$output_file"

  if [ $? -ne 0 ]; then
    echo "Error converting '$file'"
  fi
done

echo "Conversion process completed."