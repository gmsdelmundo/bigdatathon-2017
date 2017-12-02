#!/bin/bash

if [ -e kv-data ]; then
    rm kv-data
fi

touch kv-data

echo "Aggregating CSV records"
for csv in ./*3.csv; do
    echo "Now looping through $csv"
    while read line; do
        echo $line >> kv-data
    done < $csv
done
