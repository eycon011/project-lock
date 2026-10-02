"""database.py

Cria e gerencia o banco de dados SQLite com o historico de uso da fechadura.
"""

import sqlite3
from datetime import datetime

from config import BANCO_DADOS


def inicializar_banco():
    conexao = sqlite3.connect(BANCO_DADOS)
    cursor = conexao.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT NOT NULL,
            estado_porta TEXT NOT NULL,
            estado_tranca TEXT NOT NULL
        )
        """
    )
    conexao.commit()
    conexao.close()


def registrar_evento(estado_porta, estado_tranca):
    conexao = sqlite3.connect(BANCO_DADOS)
    cursor = conexao.cursor()
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO eventos (data_hora, estado_porta, estado_tranca) VALUES (?, ?, ?)",
        (agora, estado_porta, estado_tranca),
    )
    conexao.commit()
    conexao.close()
    print(f"[{agora}] Porta: {estado_porta} | Tranca: {estado_tranca}")


def listar_historico(limite=20):
    conexao = sqlite3.connect(BANCO_DADOS)
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT data_hora, estado_porta, estado_tranca FROM eventos ORDER BY id DESC LIMIT ?",
        (limite,),
    )
    resultados = cursor.fetchall()
    conexao.close()
    return resultados
