"""sensors.py

Abstrai a leitura dos sensores de porta e tranca.

Se a biblioteca RPi.GPIO estiver disponivel E o modo simulado estiver
desligado (MODO_SIMULADO = False em config.py), o codigo usa os pinos
fisicos do Raspberry Pi de verdade.

Caso contrario, cai automaticamente no modo simulado, para voce poder
testar toda a logica do programa no VSCode, no seu PC, sem nenhum
hardware conectado.
"""

import random
import time

from config import PINO_SENSOR_PORTA, PINO_SENSOR_TRANCA, PINO_RELE, MODO_SIMULADO

USANDO_HARDWARE_REAL = False
GPIO = None

if not MODO_SIMULADO:
    try:
        import RPi.GPIO as GPIO  # type: ignore

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PINO_SENSOR_PORTA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(PINO_SENSOR_TRANCA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(PINO_RELE, GPIO.OUT)
        GPIO.output(PINO_RELE, GPIO.LOW)
        USANDO_HARDWARE_REAL = True
    except (ImportError, RuntimeError):
        # RPi.GPIO nao existe (rodando fora de um Raspberry Pi) ou nao
        # ha permissao para acessar o GPIO. Cai para o modo simulado.
        USANDO_HARDWARE_REAL = False


# Estado usado apenas quando estamos em modo simulado
_estado_simulado = {"porta": "fechada", "tranca": "trancada"}


def ler_sensor_porta():
    """Retorna 'aberta' ou 'fechada'."""
    if USANDO_HARDWARE_REAL:
        return "fechada" if GPIO.input(PINO_SENSOR_PORTA) == GPIO.LOW else "aberta"
    return _estado_simulado["porta"]


def ler_sensor_tranca():
    """Retorna 'trancada' ou 'destrancada'."""
    if USANDO_HARDWARE_REAL:
        return "trancada" if GPIO.input(PINO_SENSOR_TRANCA) == GPIO.LOW else "destrancada"
    return _estado_simulado["tranca"]


def acionar_rele(segundos=3):
    """Aciona o rele de liberacao remota (fechadura eletrica auxiliar) por alguns segundos."""
    if USANDO_HARDWARE_REAL:
        GPIO.output(PINO_RELE, GPIO.HIGH)
        time.sleep(segundos)
        GPIO.output(PINO_RELE, GPIO.LOW)
    else:
        print(f"[SIMULADO] Rele acionado por {segundos}s (liberacao remota)")


def simular_mudanca_aleatoria():
    """So tem efeito no modo simulado - gera eventos de teste aleatorios."""
    if not USANDO_HARDWARE_REAL and random.random() < 0.3:
        _estado_simulado["porta"] = (
            "aberta" if _estado_simulado["porta"] == "fechada" else "fechada"
        )
        _estado_simulado["tranca"] = (
            "destrancada" if _estado_simulado["tranca"] == "trancada" else "trancada"
        )


def finalizar():
    """Libera os pinos GPIO ao encerrar o programa."""
    if USANDO_HARDWARE_REAL:
        GPIO.cleanup()
