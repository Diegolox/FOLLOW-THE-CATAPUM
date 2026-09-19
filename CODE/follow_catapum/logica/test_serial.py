from comunicacion_serial import ComunicacionSerial


# Ver puertos disponibles
ComunicacionSerial.imprimir_puertos()

# Crear conexión
esp32 = ComunicacionSerial(
    puerto="COM3",
    baudrate=115200,
    timeout=0.1
)

# Abrir puerto
esp32.abrir()

# Comprobar conexión
if esp32.conectado():
    print("ESP32 conectado")

# Leer una línea normal
linea = esp32.leer_linea()
print(linea)

# Leer JSON
datos = esp32.leer_json()
print(datos)

# Cerrar puerto
esp32.cerrar()