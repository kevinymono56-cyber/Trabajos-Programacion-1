from abc import ABC, abstractmethod


class Recurso(ABC):
    def __init__(self, codigo, titulo, autor):
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.prestado = False

    @abstractmethod
    def tipo(self):
        pass

    @abstractmethod
    def descripcion(self):
        pass


class Libro(Recurso):
    def __init__(self, codigo, titulo, autor, genero):
        super().__init__(codigo, titulo, autor)
        self.genero = genero

    def tipo(self):
        return "Libro"

    def descripcion(self):
        return f"[Libro] {self.titulo} - {self.autor} (Género: {self.genero})"


class Revista(Recurso):
    def __init__(self, codigo, titulo, autor, edicion):
        super().__init__(codigo, titulo, autor)
        self.edicion = edicion

    def tipo(self):
        return "Revista"

    def descripcion(self):
        return f"[Revista] {self.titulo} - {self.autor} (Edición: {self.edicion})"


class MaterialAudiovisual(Recurso):
    def __init__(self, codigo, titulo, autor, formato):
        super().__init__(codigo, titulo, autor)
        self.formato = formato

    def tipo(self):
        return "Material Audiovisual"

    def descripcion(self):
        return f"[Audiovisual] {self.titulo} - {self.autor} (Formato: {self.formato})"


class Lector:
    def __init__(self, nombre, cedula, telefono, correo):
        self.nombre = nombre
        self.cedula = cedula
        self.telefono = telefono
        self.correo = correo


class Biblioteca:
    def __init__(self):
        self.lectores = []
        self.recursos = []

        # Recursos preestablecidos
        self.recursos.append(Libro("A001", "El Quijote", "Miguel de Cervantes", "Novela"))
        self.recursos.append(Revista("E002", "Scientific American", "Varios", "Enero 1845"))
        self.recursos.append(MaterialAudiovisual("I001", "La La Land", "Damien Chazelle", "DVD"))

    def registrar_lector(self, nombre, cedula, telefono, correo):
        lector = Lector(nombre, cedula, telefono, correo)
        self.lectores.append(lector)
        return f"Lector {nombre} registrado con éxito."

    def agregar_recurso(self, recurso):
        self.recursos.append(recurso)
        return f"Recurso '{recurso.titulo}' agregado con éxito."

    def prestar_recurso(self, codigo):
        for recurso in self.recursos:
            if recurso.codigo == codigo:
                if recurso.prestado:
                    return f"El recurso '{recurso.titulo}' ya está prestado."
                else:
                    recurso.prestado = True
                    return f"Recurso '{recurso.titulo}' prestado con éxito."
        return "Recurso no encontrado."

    def devolver_recurso(self, codigo):
        for recurso in self.recursos:
            if recurso.codigo == codigo:
                if recurso.prestado:
                    recurso.prestado = False
                    return f"Recurso '{recurso.titulo}' devuelto con éxito."
                else:
                    return f"El recurso '{recurso.titulo}' no estaba prestado."
        return "Recurso no encontrado."


def menu():
    biblioteca = Biblioteca()

    while True:
        print("\n--- Biblioteca ---")
        print("1. Registrar Lector")
        print("2. Agregar Recurso")
        print("3. Prestar Recurso")
        print("4. Devolver Recurso")
        print("5. Listar Recursos")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            cedula = input("Cédula: ")
            telefono = input("Teléfono: ")
            correo = input("Correo: ")
            print(biblioteca.registrar_lector(nombre, cedula, telefono, correo))

        elif opcion == "2":
            print("\nTipo de recurso:")
            print("1. Libro")
            print("2. Revista")
            print("3. Material Audiovisual")
            tipo = input("Seleccione: ")

            codigo = input("Código: ")
            titulo = input("Título: ")
            autor = input("Autor: ")

            if tipo == "1":
                genero = input("Género: ")
                recurso = Libro(codigo, titulo, autor, genero)
            elif tipo == "2":
                edicion = input("Edición: ")
                recurso = Revista(codigo, titulo, autor, edicion)
            elif tipo == "3":
                formato = input("Formato: ")
                recurso = MaterialAudiovisual(codigo, titulo, autor, formato)
            else:
                print("Opción no válida.")
                continue

            print(biblioteca.agregar_recurso(recurso))

        elif opcion == "3":
            codigo = input("Código del recurso a prestar: ")
            print(biblioteca.prestar_recurso(codigo))

        elif opcion == "4":
            codigo = input("Código del recurso a devolver: ")
            print(biblioteca.devolver_recurso(codigo))

        elif opcion == "5":
            print("\n--- Recursos en la Biblioteca ---")
            for recurso in biblioteca.recursos:
                estado = "Prestado" if recurso.prestado else "Disponible"
                print(f"{recurso.codigo} - {recurso.descripcion()} - Estado: {estado}")

        elif opcion == "6":
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida, intente de nuevo.")


if __name__ == "__main__":
    menu()
