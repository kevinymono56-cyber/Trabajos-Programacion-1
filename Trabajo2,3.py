#kevin ospina villada
# Función para extraer subcadenas según el tipo de carácter inicial
def extraer_subcadenas(texto, tipo_caracter):
    letras_vocales = "aeiouAEIOU"
    lista_subcadenas = []  # Lista para guardar las subcadenas encontradas
    
    for posicion in range(len(texto)):
        caracter_actual = texto[posicion]
        
        if tipo_caracter == "vocal":
            es_vocal = caracter_actual in letras_vocales
            if es_vocal:
                for fin in range(posicion + 1, len(texto) + 1):
                    lista_subcadenas.append(texto[posicion:fin])
        elif tipo_caracter == "consonante":
            es_consonante = caracter_actual not in letras_vocales
            if es_consonante:
                for fin in range(posicion + 1, len(texto) + 1):
                    lista_subcadenas.append(texto[posicion:fin])
    
    return lista_subcadenas

# Solicitar entrada del usuario
texto_entrada = input("Ingrese la cadena: ")

# Generar subcadenas para cada jugador
# Jugador A: subcadenas que empiezan con vocal
lista_jugador_A = extraer_subcadenas(texto_entrada, "vocal")
# Jugador B: subcadenas que empiezan con consonante
lista_jugador_B = extraer_subcadenas(texto_entrada, "consonante")

# Calcular puntuaciones
puntos_A = len(lista_jugador_A)
puntos_B = len(lista_jugador_B)

# Determinar y mostrar el resultado
if puntos_A > puntos_B:
    print(f"El ganador es el jugador A con un total de {puntos_A} subcadenas")
elif puntos_B > puntos_A:
    print(f"El ganador es el jugador B con un total de {puntos_B} subcadenas")
else:
    print(f"Empate {puntos_A}")

# Mostrar detalles de las subcadenas
print("\nEstas son las subcadenas: ")
print("\nSubcadenas de A (vocales):", lista_jugador_A)
print("Subcadenas de B (consonantes):", lista_jugador_B)