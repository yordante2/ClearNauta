import imaplib

def main():
    print("Bienvenido al sistema de gestión de correos.")
    usuario = input("Ingrese su usuario: ")
    contraseña = input("Ingrese su contraseña: ")

    try:
        # Conexión al servidor IMAP sin SSL
        server = imaplib.IMAP4("imap.nauta.cu", 143)
        server.login(usuario, contraseña)
        print("Conexión establecida correctamente.")

        # Recupera las carpetas disponibles
        status, carpetas = server.list()
        if status != "OK":
            print("No se pudieron obtener las carpetas.")
            return

        mensajes_totales = 0

        for carpeta in carpetas:
            carpeta_nombre = carpeta.decode().split(' "/" ')[-1]
            print(f"Revisando carpeta: {carpeta_nombre}")

            # Seleccionar la carpeta actual
            server.select(carpeta_nombre)

            # Buscar todos los mensajes en la carpeta
            status, mensajes = server.search(None, "ALL")
            mensajes_ids = mensajes[0].split()
            cantidad_mensajes = len(mensajes_ids)
            mensajes_totales += cantidad_mensajes

            print(f"Hay {cantidad_mensajes} mensajes en la carpeta {carpeta_nombre}.")

            # Pregunta al usuario si desea borrar los mensajes de esta carpeta
            if cantidad_mensajes > 0:
                opcion = input(f"¿Desea borrar los mensajes de la carpeta {carpeta_nombre}? (S/N): ").strip().upper()
                if opcion == "S":
                    for num in mensajes_ids:
                        server.store(num, '+FLAGS', '\\Deleted')
                    server.expunge() # Elimina los correos marcados
                    print(f"Mensajes eliminados de la carpeta {carpeta_nombre}.")
                else:
                    print(f"No se eliminaron los mensajes de la carpeta {carpeta_nombre}.")

        print(f"Operación completada. Mensajes totales procesados: {mensajes_totales}")

        # Cierra la conexión
        server.close()
        server.logout()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
