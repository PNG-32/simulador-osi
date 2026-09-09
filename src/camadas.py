class CamadaOSI:
    def __init__(self, nome):
        self.nome = nome

    def encapsular(self, dados):
        # Adiciona o cabeçalho da camada atual aos dados
        return f"[{self.nome} Header] + ({dados})"

    def decapsular(self, dados):
        # Remove o cabeçalho da camada atual
        partes = dados.split(" + ")
        return partes[1][1:-1] if len(partes) > 1 else dados

# As 7 camadas do modelo
camadas = [
    CamadaOSI("7 - Aplicação"),
    CamadaOSI("6 - Apresentação"),
    CamadaOSI("5 - Sessão"),
    CamadaOSI("4 - Transporte"),
    CamadaOSI("3 - Rede"),
    CamadaOSI("2 - Enlace"),
    CamadaOSI("1 - Física")
]

# Camada 7
# Gerar a mensagem e identificar o
# processo pelo nome (endereço específico).
class Lay_7:
    def criar_mens():
        input_string = input('Digite um número: ')
        dados_atuais = Lay_6.Criptografar(input_string)
        return print(dados_atuais)

# Camada 6
# Converter texto em sequência de octetos, registrar o esquema de codificação 
# e cifrar o conteúdo, que só é decifrado na camada 6 do destino.
class Lay_6:
    def Criptografar(message):
        hex_value = message.encode('utf-8').hex()
        return hex_value

# Camada 5
# Abrir, manter e encerrar o diálogo,
# atribuindo um identificador de sessão.
class Lay_5:
    def template():
        return 

# Camada 4
#Numerar portas de origem e destino,
#segmentar a mensagem em pelo menos
#três segmentos numerados quando ela
#exceder o limite adotado, e remontá-los
#em ordem na camada 4 do destino
class Lay_4:
    def template_2():
        return 

# Camada 3
# Inserir o par de endereços lógicos e
# consultar a tabela de encaminhamento.
class Lay_3:
    def template_3():
        return 

# Camada 2
# Inserir o par de endereços físicos do salto,
# delimitar o quadro e calcular a
# verificação de erro.
class Lay_2:
    def template_4():
        return 
    
# Camada 1
# Converter o quadro em uma sequência de
# bits e transportá-la pelo enlace 
class Lay_1:
    def template_5():
        return 