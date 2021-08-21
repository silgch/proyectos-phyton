#¿Cuál es mi acrónimo?
#Vamos a pedir al usuario que ingrese el significado completo de una organización o concepto y con ello como resultado obtendremos el acrónimo. Por ejemplo:

#Entrada -> As Soon As Possible. Salida -> ASAP.
#Entrada -> World Health Organization. Salida -> WHO.
#Entrada -> Absent Without Leave. Salida -> AWOL.

def acronimo (unaFrase):
    primerasLetras= list(map(primeraLetra, unaFrase.split()))
    acronimo=""
    for letra in primerasLetras:
        acronimo= acronimo+letra

    return acronimo
primeraLetra = lambda x: x[0]


if __name__ == '__main__':
    print("Escribe una frase de la que quieres saber su acronimo o enter para salir: ")
    unaFrase = input()

    while(len(unaFrase)!=1):

        print(f"El acronimo es: {acronimo(unaFrase)}")
        print("Escribe una frase de la que quieres saber su acronimo o enter para salir: ")
        unaFrase = input()
