#!/bin/bash

while read line
do
    echo $line
done

# Desde el terminal debo darle permisos con
# chmod 777 students_generator.sh
# para probarlo debemos hacer ./students_generator.hs < MOCK_DATA.csv