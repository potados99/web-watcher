#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

source $DIR/exports.sh
python3.7 main.py --target 'https://tktapi.melon.com/api/product/schedule/list.json?prodId=206425&pocCode=SC0003&perfTypeCode=GN0001&sellTypeCode=ST0001&corpCodeNo=&v=1' --interval 0.2 --recipient '01029222661'
