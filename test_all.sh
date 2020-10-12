#!/bin/bash

tests=(
    "00"
    "01"
    "02"
    "03"
    "04"
    "05"
    "06"
    "07"
    "08"
    "09"
    "10"
    "11"
    "12"
    "13"
    "14"
)
TARGET="$(pwd)/tests_parser/test"
for test in "${tests[@]}"; do
    echo "$TARGET$test"
    INPUT_NAME="${TARGET}${test}.input"
    EXPECTED_NAME="${TARGET}${test}.expected"
    OUTPUT_NAME="${TARGET}${test}.output"
    DIFF_NAME="${TARGET}${test}.diff"

    python parser.py $INPUT_NAME > $OUTPUT_NAME
    diff $EXPECTED_NAME $OUTPUT_NAME > $DIFF_NAME
    if [ $? != 0 ]
    then
        echo "test: $TARGET$test failed"
    fi
done
