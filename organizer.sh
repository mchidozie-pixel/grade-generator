#!/bin/bash
# organizer.sh
# Archive CSV files with timestamps

mkdir -p archive

timestamp=$(date +"%Y%m%d_%H%M%S")

for file in *.csv; do
    if [ -e "$file" ]; then
        new_name="${file%.*}_$timestamp.csv"
        mv "$file" "archive/$new_name"
        echo "Moved $file → archive/$new_name"
    fi
done
