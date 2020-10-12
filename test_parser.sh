#!/bin/bash

TARGET=$1
INPUT_NAME="${TARGET}.input"
EXPECTED_NAME="${TARGET}.expected"
OUTPUT_NAME="${TARGET}.output"

python parser.py $INPUT_NAME > $OUTPUT_NAME

diff $EXPECTED_NAME $OUTPUT_NAME
