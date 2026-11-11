import random


n = int(input("Ingrese el valor de n: "))
# Leemos el la cantidad de elementos que queremos ordenar

lista = []
ordenado = []
# Creamos la lista que ordenaremos y otra para compararla

for i in range(n+1):
    lista.append(i)
    ordenado.append(i)
# Llenamos la lista

print(*lista)

for i in range(len(lista) - 1, 0, -1):
        j = int(random.random() * (i + 1))
        lista[i], lista[j] = lista[j], lista[i]
# Mezclamos de forma aleatoria los numeros

print(*lista)

# Por la naturaleza del BogoSort, seguiremos mezcando al azar el arreglo hasta que este en orden

while (lista != ordenado):
    for i in range(len(lista) - 1, 0, -1):
        j = int(random.random() * (i + 1))
        lista[i], lista[j] = lista[j], lista[i]
    print(*lista)
