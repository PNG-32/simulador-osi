import json
from dispositivos import *
from rede import *

dispositivos = carregar_dispositivos()
print('\nMaquina de OSI\n')

while True:
    origem_nome = input('Qual o computador de origem?: ')
    origem = dispositivos.get(origem_nome)
    if origem is None:
        print('Dispositivo de origem invalido')
        continue

    mensagem = input('Digite a mensagem: ')
    while True:
        destino_nome = input('Qual o destino da sua mensagem?: ')
        destino = dispositivos.get(destino_nome)
        if destino is None:
            print('Dispositivo de destino invalido')
        elif destino_nome == origem_nome:
            print('Não e possivel enviar no mesmo dispositivo')
        else:
            print('\nProcessando...\n')
            origem.enviar(mensagem, destino_nome)
        break
    break
    
