"""Configuracoes do sistema - ajuste conforme sua instalacao."""

# Modo simulado: True para testar no VSCode sem hardware conectado.
# Mude para False quando estiver rodando no Raspberry Pi real com os sensores ligados.
MODO_SIMULADO = True

# Pinagem GPIO (numeracao BCM) - so e usada quando MODO_SIMULADO = False
PINO_SENSOR_PORTA = 17
PINO_SENSOR_TRANCA = 27
PINO_RELE = 22

# Intervalo entre leituras dos sensores (em segundos)
INTERVALO_LEITURA = 1

# Nome do arquivo do banco de dados SQLite
BANCO_DADOS = "fechadura.db"
