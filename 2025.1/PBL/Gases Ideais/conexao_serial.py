import serial
from time import sleep

# Nome do arquivo onde os dados serão salvos
NOME_DO_ARQUIVO = "medidas.txt"

# Configurações da porta serial
BAUD_RATE = 9600
PORTA_SERIAL = "COM3"  # ou '/dev/ttyACM0' no Linux

# Aguarda a porta serial estabilizar (importante para o Leonardo e Micro)
sleep(2)

try:
    with serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1) as pserial:
        print("Conectado. Lendo dados...\n")
        sleep(2)  # espera o Arduino reiniciar após abertura da serial
        while True:
            if pserial.in_waiting > 0:
                line = pserial.readline().decode("utf-8").strip()
                print(line)
                with open(NOME_DO_ARQUIVO, "a") as arquivo:
                    arquivo.write(line + "\n")
except serial.SerialException as e:
    print(f"Erro de comunicação serial: {e}")
