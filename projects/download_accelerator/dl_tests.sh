#!/bin/bash

urls=$@

getopt --test > /dev/null
if [[ $? -ne 4 ]]; then
    echo "I’m sorry, `getopt --test` failed in this environment."
    exit 1
fi

SHORT=dgu:t:
LONG=debug,gov,url:,threads
PARSED=`getopt --options $SHORT --longoptions $LONG --name "$0" -- "$@"`

if [[ $? -ne 0 ]]; then
    # e.g. $? == 1
    #  then getopt has complained about wrong arguments to stdout
    echo 'bad arguments'
    exit 2
fi

eval set -- "$PARSED"

while true; do
    case "$1" in
        -d|--debug)
            d='-d'
            shift
            ;;
        -g|--gov)
            g=y
            shift
            ;;
        -u|--url)
            u=y
            link=$2
            shift 2
            ;;
        -t|--threads)
            t=$2
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Programming error"
            exit 3
            ;;
    esac
done

if [[ $# -ge 1 ]]; then
    echo 'Extra argumets given:'
    echo "$@"
fi

echo "gov: $f, debug: $d, link: $link, threads: $t"

if [ -n "$g" ]; then
    # set the urls to the government ones
    urls=('http://www2.census.gov/geo/tiger/TIGER2013/TRACT/tl_2013_10_tract.zip'
            'http://www2.census.gov/geo/tiger/TIGER2013/EDGES/tl_2013_35005_edges.zip'
            'http://www2.census.gov/geo/tiger/TGRGDB13/tlgdb_2013_a_39_oh.gdb.zip')
else
    urls=($link)
fi

for url in "${urls[@]}"; do
    for num in 1 2 5 $t; do
        echo
        echo "Downloading: $url with {$num} thread(s)"
        python download_accelerator.py $d -n$num $url
    done
done

