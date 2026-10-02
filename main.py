"""main.py

Loop principal do sistema de monitoramento da fechadura.
Fica rodando continuamente, le os sensores e registra qualquer mudanca
de estado (porta e/ou tranca) no banco de dados.

Como rodar (dentro do VSCode, no terminal integrado):
    python main.py

Para ver o historico ja salvo:
    python main.py --historico
"""

import sys
import time

from config import INTERVALO_LEITURA
import sensors
import database


def main():
    database.inicializar_banco()
    modo = "SIMULADO (sem hardware)" if not sensors.USANDO_HARDWARE_REAL else "HARDWARE REAL"
    print(f"Sistema de monitoramento iniciado - modo: {modo}")
    print("Pressione Ctrl+C para sair.\n")

    ultimo_estado_porta = None
    ultimo_estado_tranca = None

    try:
        while True:
            sensors.simular_mudanca_aleatoria()  # so tem efeito no modo simulado

            estado_porta = sensors.ler_sensor_porta()
            estado_tranca = sensors.ler_sensor_tranca()

            mudou = (
                estado_porta != ultimo_estado_porta
                or estado_tranca != ultimo_estado_tranca
            )

            if mudou:
                database.registrar_evento(estado_porta, estado_tranca)
                ultimo_estado_porta = estado_porta
                ultimo_estado_tranca = estado_tranca

            time.sleep(INTERVALO_LEITURA)

    except KeyboardInterrupt:
        print("\nEncerrando...")
    finally:
        sensors.finalizar()


def mostrar_historico():
    eventos = database.listar_historico()
    if not eventos:
        print("Nenhum evento registrado ainda.")
        return
    print(f"{'Data/Hora':<20} {'Porta':<12} {'Tranca':<12}")
    print("-" * 44)
    for data_hora, porta, tranca in eventos:
        print(f"{data_hora:<20} {porta:<12} {tranca:<12}")


if __name__ == "__main__":
    if "--historico" in sys.argv:
        mostrar_historico()
    else:
        main()
