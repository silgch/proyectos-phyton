# Piedra, Papel, Tijeras

import numpy as np
import string
puntos_jugador=0
puntos_computadora = 0

def ganador(eleccionJugador):
    global puntos_jugador
    global puntos_computadora

    if(not (eleccionJugador) in ['tijera', 'piedra', 'papel']) :
        return "Jugada no permitida"
    computador = np.random.choice(['tijera', 'piedra', 'papel'])

    if eleccionJugador == computador:
        return ('Empate en:', eleccionJugador)
    else:
        if ((eleccionJugador == 'piedra' and computador == 'tijera') or (eleccionJugador == 'tijera' and computador == 'papel') or (
            eleccionJugador == 'papel' and computador == 'piedra')):
            puntos_jugador += 1
            return ('Jugador ganó:', eleccionJugador, 'vs', computador)
        else:
            puntos_computadora += 1
            return ('Computadora ganó:', eleccionJugador, 'vs', computador)

def definirJugada(numero):
    if(numero=='1') : return "piedra"
    if(numero=='2') : return "papel"
    if(numero=='3') : return "tijera"
    else: return ""

if __name__ == '__main__':


    print("BIENVENIDO! \n Elija su jugada:\n 1) Piedra    2) Papel    3) Tijera\n Presione Enter para salir")
    numero= input()

    while(numero != ""):

        eleccionJugador= definirJugada(numero)
        print(ganador(eleccionJugador))
        print(f"Estado del juego:\n Computadora: {puntos_computadora} - Jugador: {puntos_jugador}\n")
        print("Elija su jugada:\n 1) Piedra    2) Papel    3) Tijera")
        numero = input()
