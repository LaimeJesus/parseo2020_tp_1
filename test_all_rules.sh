#!/bin/bash

reglas=(
    "1"
    "2"
    "3"
    "4"
)

tests=(
    "ejemplo_1"
    "ejemplo_2"
    "ejemplo_3"
    "ejemplo_4"
)
TARGET="$(pwd)/tests_regla"
for regla in "${reglas[@]}"; do
    CURRENT_RULE="${TARGET}_${regla}"
    echo "Testing rule: ${CURRENT_RULE}"
    for test in "${tests[@]}"; do
        CURRENT_TEST="${CURRENT_RULE}/${test}"
        echo "test: ${CURRENT_TEST}"
        INPUT_NAME="${CURRENT_TEST}.input"
        EXPECTED_NAME="${CURRENT_TEST}.expected"
        OUTPUT_NAME="${CURRENT_TEST}.output"
        DIFF_NAME="${CURRENT_TEST}.diff"

        python parser.py $INPUT_NAME > $OUTPUT_NAME
        diff $EXPECTED_NAME $OUTPUT_NAME > $DIFF_NAME
        if [ $? != 0 ]
        then
            echo "test: ${CURRENT_TEST} failed"
        fi
    done
done
