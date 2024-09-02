import ipaddress
import os

class Red:
    def __init__(self, direccion_ip, mascara, prefijo):
        """
        Clase que representa una red IPv4.

        Args:
        - direccion_ip (str): Dirección IP de la red.
        - mascara (int): Longitud de la máscara de subred.
        - prefijo (int): Prefijo de la máscara de subred.
        """
        self.direccion_ip = ipaddress.IPv4Address(direccion_ip)
        self.mascara = int(mascara)
        self.prefijo = int(prefijo)

    def obtener_direccion_de_red(self):
        """
        Obtiene la dirección de red de la instancia.

        Returns:
        - IPv4Address: Dirección de red.
        """
        red = ipaddress.ip_network(f"{self.direccion_ip}/{self.mascara}", strict=False)
        return red.network_address

    def obtener_broadcast(self):
        """
        Obtiene la dirección de broadcast de la instancia.

        Returns:
        - IPv4Address: Dirección de broadcast.
        """
        
        red = ipaddress.ip_network(f"{self.direccion_ip}/{self.mascara}", strict=False)
        return red.broadcast_address

    def obtener_numero_de_ips(self):
        """
        Obtiene el número total de direcciones IP en la red.

        Returns:
        - int: Número total de direcciones IP.
        """
        
        red = ipaddress.ip_network(f"{self.direccion_ip}/{self.mascara}", strict=False)
        return red.num_addresses

    def obtener_ips_disponibles(self):
        """
        Obtiene una lista de direcciones IP disponibles en la red.

        Returns:
        - list: Lista de direcciones IP disponibles.
        """
        
        red = ipaddress.ip_network(f"{self.direccion_ip}/{self.mascara}", strict=False)
        direcciones_disponibles = [str(ip) for ip in red.hosts()]
        return direcciones_disponibles

    def obtener_rango_y_num_hosts(self):
        """
        Obtiene el rango de direcciones IP y el número de hosts en la red.

        Returns:
        - tuple: Tupla con el rango y el número de hosts.
        """
        
        red = ipaddress.ip_network(f"{self.direccion_ip}/{self.mascara}", strict=False)
        rango = f"{red.network_address} - {red.broadcast_address}"
        num_hosts = red.num_addresses - 2  # Restamos la dirección de red y de broadcast
        return rango, num_hosts


class RedSubred(Red):
    def __init__(self, direccion_ip, mascara, prefijo, num_subredes):
        """
        Clase que representa una red con subredes.

        Args:
        - direccion_ip (str): Dirección IP base.
        - mascara (int): Máscara de subred original.
        - prefijo (int): Prefijo de la máscara original.
        - num_subredes (int): Número de subredes a crear.
        """
        
        super().__init__(direccion_ip, mascara, prefijo)
        self.num_subredes = num_subredes

    def obtener_ips_disponibles_por_subred(self):
        """
        Obtiene una lista de listas con direcciones IP disponibles en cada subred.

        Returns:
        - list: Lista de listas con direcciones IP disponibles.
        """
        
        direcciones_disponibles = []
        for i in range(self.num_subredes):
            nueva_mascara = self.mascara + i
            nueva_red = Red(self.direccion_ip, nueva_mascara, self.prefijo)
            direcciones_disponibles.append(nueva_red.obtener_ips_disponibles())
        return direcciones_disponibles


class ArchivoRed:
    @staticmethod
    def crear_archivo(info_red):
        """
        Crea un archivo de texto con la información de la red.

        Args:
        - info_red (Red o RedSubred): Instancia de Red o RedSubred.

        Returns:
        - str: Ruta del archivo creado.
        """
        
        # Crear una carpeta para los archivos de red si no existe
        carpeta_salida = "archivos_red"
        os.makedirs(carpeta_salida, exist_ok=True)
        
        # Crear el nombre del archivo usando la dirección IP
        ruta_archivo = os.path.join(carpeta_salida, "informacion_red.txt")
        with open(ruta_archivo, "w") as archivo:
            archivo.write(f"Dirección de Red: {info_red.obtener_direccion_de_red()}\n")
            archivo.write(f"Dirección de Broadcast: {info_red.obtener_broadcast()}\n")
            archivo.write(f"Número de saltos en la subred: {info_red.obtener_numero_de_ips()}\n")
            archivo.write("Direcciones IP disponibles en cada subred:\n")

            direcciones_disponibles = info_red.obtener_ips_disponibles()
            for i, ip in enumerate(direcciones_disponibles, start=1):
                archivo.write(f"Subred {i}: {ip}\n")
                
                rango, num_hosts = Red(ip, info_red.mascara, info_red.prefijo).obtener_rango_y_num_hosts()
                archivo.write(f"  Rango de direcciones IP: {rango}\n")
                archivo.write(f"  Número de hosts: {num_hosts}\n")

        return ruta_archivo  # Devolvemos la ruta del archivo creado

    @staticmethod
    def leer_archivo(ruta_archivo):
        """
        Lee el contenido de un archivo de texto.

        Args:
        - ruta_archivo (str): Ruta del archivo a leer.
        """
        try:
            with open(ruta_archivo, "r") as archivo:
                contenido = archivo.read()
                print(contenido)
        except FileNotFoundError:
            print("No se encontró el archivo de información de red.")

def main():
    red = None
    ruta_archivo = None
    while True:
        print("""
              -------------------
              *******************
              MENÚ PRINCIPAL
              -------------------
              *******************
              1. Crear Información de Red
              2. Mostrar Información de Red
              3. Salir
              """)

        opcion = input("Ingrese la opción deseada: ")

        if opcion == "1":
            direccion_ip = input("Ingrese la dirección IP base: ")
            mascara_prefijo = int(input("Ingrese la máscara de subred en formato prefijo (ej. 24): "))
            num_subredes = int(input("Ingrese la cantidad de bits a encender:  "))

            # Calcular la nueva máscara y crear la instancia
            bits = num_subredes.bit_length()
            nueva_mascara = mascara_prefijo + bits

            red = RedSubred(direccion_ip, nueva_mascara, mascara_prefijo, num_subredes) if num_subredes > 0 else Red(direccion_ip, mascara_prefijo, mascara_prefijo)

            # Crear el archivo y guardar la ruta
            ruta_archivo = ArchivoRed.crear_archivo(red)
            print("Información de red creada y guardada en el archivo:", ruta_archivo)

        elif opcion == "2":
            if red is not None and ruta_archivo is not None:
                ArchivoRed.leer_archivo(ruta_archivo)
                print(f"\nNueva máscara de subred para {red.num_subredes} subredes: /{red.mascara}")
                print(f"Nueva dirección de red: {red.obtener_direccion_de_red()}")
                print(f"Nueva dirección de Broadcast: {red.obtener_broadcast()}")
                print(f"Número de saltos en cada subred: {red.obtener_numero_de_ips()}")

                direcciones_disponibles = red.obtener_ips_disponibles()
                print("\nInformación detallada de cada subred:")
                for i, ip in enumerate(direcciones_disponibles, start=1):
                    print(f"\nSubred {i}: {ip}")

                    rango, num_hosts = Red(ip, red.mascara, red.prefijo).obtener_rango_y_num_hosts()
                    print(f"  Rango de direcciones IP: {rango}")
                    print(f"  Número de hosts: {num_hosts}")

            else:
                print("No se ha creado información de red. Por favor, seleccione la opción 1 primero.")

        elif opcion == "3":
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida. Por favor, ingrese una opción válida.")

if __name__ == "__main__":
    main()
