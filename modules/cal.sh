#!/bin/bash

# Función para calcular si un año es bisiesto
is_leap_year() {
    year=$1
    if (( year % 4 == 0 && year % 100 != 0 )) || (( year % 400 == 0 )); then
        echo 1
    else
        echo 0
    fi
}

# Función para obtener el número de días en un mes
days_in_month() {
    month=$1
    year=$2
    case $month in
        1|3|5|7|8|10|12) echo 31 ;;
        4|6|9|11) echo 30 ;;
        2)
            if (( $(is_leap_year $year) == 1 )); then
                echo 29
            else
                echo 28
            fi
            ;;
    esac
}

# Función para obtener el día de la semana del primer día del mes
first_day_of_month() {
    month=$1
    year=$2
    # Ajustar el mes y el año para Zeller's Congruence
    if (( month < 3 )); then
        month=$((month + 12))
        year=$((year - 1))
    fi
    q=1
    K=$((year % 100))
    J=$((year / 100))
    h=$(( (q + (13 * (month + 1)) / 5 + K + K / 4 + J / 4 + 5 * J) % 7 ))
    # Ajustar para que 0 = sábado, 1 = domingo, ..., 6 = viernes
    day_of_week=$(( (h + 6) % 7 ))
    echo $day_of_week
}

# Obtener el mes y el año actuales
month=$(date +%m)
year=$(date +%Y)
month=$(echo $month | sed 's/^0//')  # Quitar ceros a la izquierda

# Calcular el número de días en el mes y el primer día del mes
days=$(days_in_month $month $year)
start_day=$(first_day_of_month $month $year)

# Imprimir el encabezado del calendario
echo "Do Lu Ma Mi Ju Vi Sa"

# Imprimir espacios para los días antes del primer día del mes
for ((i=0; i<$start_day; i++)); do
    echo -n "   "
done

# Imprimir los días del mes
for ((day=1; day<=$days; day++)); do
    printf "%2d " $day
    if (( (start_day + day) % 7 == 0 )); then
        echo  # Nueva línea después del sábado
    fi
done