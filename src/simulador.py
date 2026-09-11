import json
from dispositivos import *
from rede import *

Active = True
dispositivos = carregar_dispositivos()
print('\nMaquina de OSI')

while Active:
    origem_nome = input('\nQual o computador de origem?: ')
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
            while True:
                error_dec = input('Deseja inserir um erro na conexão? (y/n): ').lower()
                if error_dec == "y":
                    armar_erro_de_transmissao(origem_nome, destino_nome)
                    break
                elif error_dec == "n":
                    break
                else:
                    print('Comando Invalido')
            print('\nProcessando...\n')
            origem.enviar(mensagem, destino_nome)
        break  

    while True:
            dec = input('Deseja enviar mais alguma mensagem? (y/n): ').lower()
            if dec == "y":
                break
            elif dec == "n":
                print('\nDesligando...\n')
                Active = False
                break
            else:
                print('Comando Invalido')
    
