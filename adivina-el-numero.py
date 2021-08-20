# Juego : Adivinar un número aleatorio.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import random


def adivina_el_numero(x):
    # Use a breakpoint in the code line below to debug your script.
    numero_aleatorio = random.randint(1, x)
    prediccion = 0

    while prediccion != numero_aleatorio:
        prediccion = int(input(f"Adivina un numero entre 1 y {x}:"))  # Este tipo de formato se llama f-string
        if prediccion < numero_aleatorio:
            print("Intenta otra vez, este numero es muy pequeño.")
        elif prediccion > numero_aleatorio:
            print("Intenta otra vez, este numero es muy grande.")

    print(f" Adivinaste el numero: {prediccion}.")




if __name__ == '__main__':
    print("Bienvenido! El juego elije en adivinar un número entre 1 el número que elijas")
    x= int(input('El numero será inferior a: '))
    adivina_el_numero(x)