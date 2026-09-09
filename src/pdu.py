from dispositivos import carregar_dispositivos

dispositivos = carregar_dispositivos()
origem_nome = input('Qual o computador de origem?: ')
origem = dispositivos.get(origem_nome)

if origem is None:
    print('Dispositivo de origem invalido')
else:
    mensagem = input('Digite a mensagem: ')
    destino_nome = input('Qual o destino da sua mensagem?: ')
    origem.enviar(mensagem, destino_nome)