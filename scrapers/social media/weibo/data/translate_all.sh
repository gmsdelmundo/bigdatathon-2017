#/bin/bash

if [ -e translated_items.txt ]; then
    rm translated_items.txt
fi

echo "Looping through all CSV files"
for csv in ../data/*.csv; do
    echo "Now looping through $csv"
    while read line; do
        echo "Translating $line"
        python translate_to_chinese.py "$line" >> translated_items.txt
    done < $csv
done
