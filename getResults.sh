#!/bin/bash

for i in `seq 1 10`;
do
    COUNTER=$(($i * 100))
    echo $COUNTER
    python DBConnector.py -l 1000 -tk $COUNTER -m 100000 -pp NounsLemma
done
