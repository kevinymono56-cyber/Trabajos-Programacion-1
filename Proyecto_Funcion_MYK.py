def buscar_maximo(num_listas, modulo, datos_listas):
    mejor_valor = 0
    mejor_seleccion = []

    def explorar(posicion, suma_cuadrados, elegidos):
        nonlocal mejor_valor, mejor_seleccion
        if posicion == num_listas:
            resultado = suma_cuadrados % modulo
            if resultado > mejor_valor:
                mejor_valor = resultado
                mejor_seleccion = elegidos[:]
            return
        
        for numero in datos_listas[posicion]:
            elegidos.append(numero)
            explorar(posicion + 1, suma_cuadrados + numero**2, elegidos)
            elegidos.pop()

    explorar(0, 0, [])
    return mejor_valor, mejor_seleccion


# Entrada de datos
k, m = map(int, input("Ingresa K y M separados por espacio: ").split())
listas_numeros = []
for i in range(k):
    datos = list(map(int, input(f"Lista {i+1} (el primer numero es la cantidad y se ignorará): ").split()))
    print(f"   → Ignorando el primer número ({datos[0]}), usando {datos[1:]}")
    listas_numeros.append(datos[1:])  # Ignoramos el primer número (cantidad de elementos)

# Calcular y mostrar
maximo, seleccion = buscar_maximo(k, m, listas_numeros)
print("\nValor máximo:", maximo)
print("Combinación elegida:", seleccion)
