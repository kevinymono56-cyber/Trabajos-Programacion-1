import random
from abc import ABC, abstractmethod

# ABSTRACCIÓN: Clase base Persona
class Persona(ABC):
    def __init__(self, nombre, identificacion):
        self._nombre = nombre
        self._identificacion = identificacion

    @abstractmethod
    def rol(self): pass

    def get_nombre(self): return self._nombre
    def get_identificacion(self): return self._identificacion

# HERENCIA: Pasajero hereda de Persona
class Pasajero(Persona):
    def rol(self): return "Pasajero"

# ABSTRACCIÓN: Clase base Vehículo
class Vehiculo(ABC):
    def __init__(self, id, capacidad):
        self._id = id
        self._capacidad = capacidad

    @abstractmethod
    def descripcion(self): pass

# HERENCIA: Avión hereda de Vehículo
class Avion(Vehiculo):
    def descripcion(self):
        return f"Avión {self._id} - Capacidad {self._capacidad}"

# ENCAPSULACIÓN: Clase Ticket
class Ticket:
    def __init__(self, pasajero, vuelo, clase, precio):
        self._id_ticket = str(random.randint(1000000000, 9999999999))
        self._pasajero = pasajero
        self._vuelo = vuelo
        self._clase = clase
        self._precio = precio
        self._estado = "Activo"

    def mostrar_ticket(self):
        print(f"\n=== TICKET {self._id_ticket} ===")
        print(f"Pasajero: {self._pasajero.get_nombre()} - ID: {self._pasajero.get_identificacion()}")
        print(f"Vuelo: {self._vuelo.get_codigo()} | {self._vuelo.get_origen()} → {self._vuelo.get_destino()}")
        print(f"Clase: {self._clase} | Precio: ${self._precio:,} COP")
        print(f"Duración: {self._vuelo.get_duracion()}h | Estado: {self._estado}")

    def cancelar(self): self._estado = "Cancelado"
    def get_id_ticket(self): return self._id_ticket
    def get_estado(self): return self._estado
    def get_clase(self): return self._clase
    def set_clase(self, nueva_clase): self._clase = nueva_clase
    def set_precio(self, nuevo_precio): self._precio = nuevo_precio

# POLIMORFISMO: Clase Vuelo
class Vuelo:
    def __init__(self, codigo, avion, origen, destino, duracion, capacidad_por_clase):
        self._codigo = codigo
        self._avion = avion
        self._origen = origen
        self._destino = destino
        self._duracion = duracion
        self._capacidad_por_clase = capacidad_por_clase.copy()
        self._reservas = {clase: [] for clase in capacidad_por_clase}

    def get_codigo(self): return self._codigo
    def get_origen(self): return self._origen
    def get_destino(self): return self._destino
    def get_duracion(self): return self._duracion

    def mostrar_info(self):
        print(f"\n[{self._codigo}] {self._origen} → {self._destino} ({self._duracion}h)")
        for clase, capacidad in self._capacidad_por_clase.items():
            ocupados = len(self._reservas[clase])
            precio = self.calcular_precio(clase)
            print(f"  {clase}: {ocupados}/{capacidad} asientos - ${precio:,} COP")

    def reservar(self, pasajero, clase):
        if clase not in self._capacidad_por_clase:
            return "Clase no válida."
        
        if len(self._reservas[clase]) < self._capacidad_por_clase[clase]:
            self._reservas[clase].append(pasajero)
            return Ticket(pasajero, self, clase, self.calcular_precio(clase))
        else:
            return f"Sin asientos en {clase} para vuelo {self._codigo}."

    def liberar_asiento(self, pasajero, clase):
        if clase in self._reservas and pasajero in self._reservas[clase]:
            self._reservas[clase].remove(pasajero)
            return True
        return False

    def cambiar_clase(self, pasajero, clase_actual, clase_nueva):
        if clase_nueva not in self._capacidad_por_clase:
            return False, "Clase no válida."
        
        if len(self._reservas[clase_nueva]) >= self._capacidad_por_clase[clase_nueva]:
            return False, f"Sin asientos en {clase_nueva}."
        
        if self.liberar_asiento(pasajero, clase_actual):
            self._reservas[clase_nueva].append(pasajero)
            return True, "Cambio exitoso"
        return False, "Error al cambiar."

    def calcular_precio(self, clase):
        # Precios reales colombianos
        precios_base = {
            ("Bogotá", "Medellín"): 150000,
            ("Bogotá", "Miami"): 800000,
            ("Bogotá", "Madrid"): 1500000
        }
        base = precios_base.get((self._origen, self._destino), 200000)
        
        multiplicadores = {"Económica": 1, "Comercial": 2.5, "Primera": 4.5}
        return int(base * multiplicadores.get(clase, 1))

# ENCAPSULACIÓN: Clase Aerolínea
class Aerolinea:
    def __init__(self, nombre):
        self._nombre = nombre
        self._vuelos = self._crear_catalogo()
        self._tickets_emitidos = []

    def _crear_catalogo(self):
        return [
            Vuelo("001", Avion("A320", 180), "Bogotá", "Medellín", 1, {"Económica": 100, "Comercial": 50, "Primera": 30}),
            Vuelo("002", Avion("B737", 200), "Bogotá", "Miami", 5, {"Económica": 120, "Comercial": 60, "Primera": 20}),
            Vuelo("003", Avion("A380", 400), "Bogotá", "Madrid", 10, {"Económica": 200, "Comercial": 100, "Primera": 50})
        ]

    def mostrar_vuelos(self):
        print("\n=== VUELOS DISPONIBLES ===")
        for vuelo in self._vuelos:
            vuelo.mostrar_info()

    def buscar_vuelo(self, codigo):
        return next((v for v in self._vuelos if v.get_codigo() == codigo), None)

    def agregar_ticket(self, ticket):
        self._tickets_emitidos.append(ticket)

    def buscar_ticket_por_pasajero(self, identificacion):
        return next((t for t in self._tickets_emitidos 
                    if t._pasajero.get_identificacion() == identificacion and t.get_estado() == "Activo"), None)

    def buscar_tickets_por_pasajero(self, identificacion):
        return [t for t in self._tickets_emitidos if t._pasajero.get_identificacion() == identificacion]

    def cancelar_ticket(self, identificacion):
        ticket = self.buscar_ticket_por_pasajero(identificacion)
        if not ticket:
            return "No hay ticket activo para este pasajero."
        
        vuelo = self.buscar_vuelo(ticket._vuelo.get_codigo())
        if vuelo:
            vuelo.liberar_asiento(ticket._pasajero, ticket.get_clase())
        
        ticket.cancelar()
        reembolso = int(ticket._precio * 0.8)
        return f"Ticket cancelado. Reembolso: ${reembolso:,} COP"

    def cambiar_asiento(self, identificacion, nueva_clase):
        ticket = self.buscar_ticket_por_pasajero(identificacion)
        if not ticket:
            return "No hay ticket activo para este pasajero."
        
        vuelo = self.buscar_vuelo(ticket._vuelo.get_codigo())
        clase_actual = ticket.get_clase()
        
        if clase_actual == nueva_clase:
            return f"Ya tiene asiento en {nueva_clase}."
        
        exito, _ = vuelo.cambiar_clase(ticket._pasajero, clase_actual, nueva_clase)
        
        if exito:
            nuevo_precio = vuelo.calcular_precio(nueva_clase)
            diferencia = nuevo_precio - ticket._precio
            ticket.set_clase(nueva_clase)
            ticket.set_precio(nuevo_precio)
            
            if diferencia > 0:
                return f"Cambio exitoso. Pagar: ${diferencia:,} COP"
            elif diferencia < 0:
                return f"Cambio exitoso. Reembolso: ${abs(diferencia):,} COP"
            else:
                return "Cambio exitoso. Sin diferencia de precio."
        else:
            return f"Sin asientos en {nueva_clase}."

# MENÚ PRINCIPAL
def menu():
    aerolinea = Aerolinea("SkyWings")
    
    while True:
        print("\n=== SISTEMA AEROLÍNEA ===")
        print("1. Ver vuelos  2. Reservar  3. Cancelar  4. Cambiar clase  5. Consultar  6. Salir")
        opcion = input("Opción: ")

        if opcion == "1":
            aerolinea.mostrar_vuelos()

        elif opcion == "2":
            nombre = input("Nombre: ")
            identificacion = input("ID: ")
            pasajero = Pasajero(nombre, identificacion)
            codigo = input("Código vuelo (001/002/003): ")
            vuelo = aerolinea.buscar_vuelo(codigo)

            if vuelo:
                clase_abrev = input("Clase [E]conómica/[C]omercial/[P]rimera: ").upper()
                clases = {"E": "Económica", "C": "Comercial", "P": "Primera"}
                clase = clases.get(clase_abrev)

                if clase:
                    ticket = vuelo.reservar(pasajero, clase)
                    if isinstance(ticket, Ticket):
                        aerolinea.agregar_ticket(ticket)
                        ticket.mostrar_ticket()
                        print(f"¡Reserva exitosa! Use su ID {identificacion} para gestiones.")
                    else:
                        print(ticket)
                else:
                    print("Clase no válida.")
            else:
                print("Vuelo no encontrado.")

        elif opcion == "3":
            identificacion = input("ID del pasajero: ")
            print(aerolinea.cancelar_ticket(identificacion))

        elif opcion == "4":
            identificacion = input("ID del pasajero: ")
            nueva_clase_abrev = input("Nueva clase [E]/[C]/[P]: ").upper()
            clases = {"E": "Económica", "C": "Comercial", "P": "Primera"}
            nueva_clase = clases.get(nueva_clase_abrev)
            
            if nueva_clase:
                print(aerolinea.cambiar_asiento(identificacion, nueva_clase))
            else:
                print("Clase no válida.")

        elif opcion == "5":
            identificacion = input("ID del pasajero: ")
            tickets = aerolinea.buscar_tickets_por_pasajero(identificacion)
            if tickets:
                for i, ticket in enumerate(tickets, 1):
                    print(f"\n--- Ticket {i} ---")
                    ticket.mostrar_ticket()
            else:
                print("Sin tickets para este pasajero.")

        elif opcion == "6":
            print("Gracias por usar SkyWings.")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()