#!/bin/sh

I=1

while [ "$I" != 4 ]
do
    python insert_rule.py ruletable_${I}.json
    I=$((I + 1))
done
