#!/bin/bash

for ii in $(seq -w 1 100); do
    rm -rf $ii *.png
    mkdir $ii 
    echo $ii
    python2 ./fractal-images.py $ii
    if [[ $? != 0 ]]; then
        break
    fi
    mv *.png $ii
done
