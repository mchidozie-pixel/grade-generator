#!/bin/bash
# organizer.sh
# Improved CSV (or file) archiver with timestamps

# Create archive folder if it doesn't exist
ARCHIVE_DIR="archive"
mkdir -p "$ARCHIVE_DIR"

# Get current timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Loop through all CSV files in current directory
shopt -s nullglob
for file in *.csv; do
    # Check if file exists and is not empty
    if [[ -f "$file" ]]; then
        NEW_NAME="${file%.*}_$TIMESTAMP.csv"
        mv "$file" "$ARCHIVE_DIR/$NEW_NAME"
        echo "Moved $file → $ARCHIVE_DIR/$NEW_NAME"
    fi
done

echo "All CSV files have been archived."
