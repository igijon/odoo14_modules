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
    echo "</record>"
done
echo "</odoo>"
echo "</data>"

# Desde el terminal debo darle permisos con
# chmod 777 students_generator.sh
# para probarlo debemos hacer ./students_generator.hs < MOCK_DATA.csv > demo/students.xml


# DEBEMOS QUITAR EL PRIMER RECORD PORQUE AÑADE LA FILA DE LOS TÍTULOS O NO GENERARLOS EN EL CSV