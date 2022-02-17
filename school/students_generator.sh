#!/bin/bash
echo "<odoo>"
echo "<data>"
while read line
do
    nombre=$(echo $line | cut -d',' -f1)
    dni=$(echo $line | cut -d',' -f2)
    year=$(echo $line | cut -d',' -f3)
    echo "<record id='student$dni' model='school.student'>"
    echo "<field name='name'>$nombre</field>"
    echo "<field name='dni'>$dni</field>"
    echo "<field name='birth_year'>$year</field>"
    echo "<field name='classroom' ref='school.classroom1'></field>"
    echo "<field name='photo'>$(base64 student.png)</field>"
    echo "</record>"
done
echo "</data>"
echo "</odoo>"


# Desde el terminal debo darle permisos con
# chmod 777 students_generator.sh
# para probarlo debemos hacer ./students_generator.hs < MOCK_DATA.csv > demo/students.xml

# Veremos cómo añadir las photos en las vistas más adelante
