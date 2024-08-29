#!/bin/bash

# Definición de colores
w='\e[97m'       # Blanco brillante
G1='\e[101m'     # Fondo rojo brillante
reset='\033[0m'  # Reset

# Piezas de ajedrez en Unicode (emojis)
# Piezas blancas
white_king="♔"
white_queen="♕"
white_rook="♖"
white_bishop="♗"
white_knight="♘"
white_pawn="♙"

# Piezas negras
black_king="♚"
black_queen="♛"
black_rook="♜"
black_bishop="♝"
black_knight="♞"
black_pawn="♟"

# Inicializa el tablero con las piezas en sus posiciones iniciales
init_board() {
    board=(
        "$black_rook"   "$black_knight" "$black_bishop" "$black_queen" "$black_king" "$black_bishop" "$black_knight" "$black_rook"
        "$black_pawn"   "$black_pawn"   "$black_pawn"   "$black_pawn"  "$black_pawn" "$black_pawn"   "$black_pawn"   "$black_pawn"
        " "             " "             " "             " "            " "           " "             " "             " "
        " "             " "             " "             " "            " "           " "             " "             " "
        " "             " "             " "             " "            " "           " "             " "             " "
        " "             " "             " "             " "            " "           " "             " "             " "
        "$white_pawn"   "$white_pawn"   "$white_pawn"   "$white_pawn"  "$white_pawn" "$white_pawn"   "$white_pawn"   "$white_pawn"
        "$white_rook"   "$white_knight" "$white_bishop" "$white_queen" "$white_king" "$white_bishop" "$white_knight" "$white_rook"
    )
}

# Función para mostrar el tablero
show_board() {
    clear
    for ((i = 0; i < $size; i++)); do
        for ((j = 0; j < $size; j++)); do
            index=$((i * size + j))
            piece=${board[$index]}
            
            if (( (i + j) % 2 == 0 )); then
                echo -ne "${G1} ${piece} ${reset}"
            else
                echo -ne "${w} ${piece} ${reset}"
            fi
        done
        echo "" # Nueva línea después de cada fila
    done
}

# Tamaño del tablero de ajedrez
size=8

# Movimiento de peones blancos y negros
move_white_pawns() {
    for step in {1..3}; do
        for ((i = 0; i < 8; i++)); do
            board[((6 * size) + i)]=" "         # Limpia la posición inicial del peón blanco
            board[((5 * size) + i)]="$white_pawn" # Mueve el peón blanco hacia arriba
        done
        show_board
        sleep 0.5
        for ((i = 0; i < 8; i++)); do
            board[((5 * size) + i)]=" "         # Limpia la posición del peón blanco después del movimiento
            board[((4 * size) + i)]="$white_pawn" # Mueve el peón blanco hacia arriba
        done
        show_board
        sleep 0.5
    done
}

move_black_pawns() {
    for step in {1..3}; do
        for ((i = 0; i < 8; i++)); do
            board[((1 * size) + i)]=" "         # Limpia la posición inicial del peón negro
            board[((2 * size) + i)]="$black_pawn" # Mueve el peón negro hacia abajo
        done
        show_board
        sleep 0.5
        for ((i = 0; i < 8; i++)); do
            board[((2 * size) + i)]=" "         # Limpia la posición del peón negro después del movimiento
            board[((3 * size) + i)]="$black_pawn" # Mueve el peón negro hacia abajo
        done
        show_board
        sleep 0.5
    done
}

# Inicializa el tablero
init_board

# Mueve los peones blancos y negros
move_white_pawns
move_black_pawns
