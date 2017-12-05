#/bin/sh

if [ -e query.txt ]; then
    rm query.txt
fi

touch query.txt

echo "Looping through translated items"
while read line; do
    for i in `seq 1 1`; do
        echo "$line;2015-01-01;2012-01-01;2017-12-01;$i" >> query.txt
    done
done < '../data/translated_items.txt'
