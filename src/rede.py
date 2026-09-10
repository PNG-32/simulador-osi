import json
import os

from dispositivos import Computador, Roteador

_DIR_BASE = os.path.dirname(os.path.abspath(__file__))
Topologia = os.path.join(_DIR_BASE, "topologia.json")

def _normalizar_interfaces(bruto):
    """Uniformiza o formato do topologia.json. Computador vs
    Roteador e decidido pelo formato do dado (str = uma interface,
    list = varias), nao pelo nome do dispositivo - assim o arquivo
    de topologia continua podendo ser trocado livremente (requisito
    do enunciado: trocar a rede so trocando o JSON)."""
    if isinstance(bruto["interface"], str):
        return [{
            "interface": bruto["interface"],
            "IPv4": bruto["IPv4"],
            "fisico": bruto["Physical Address"],
        }]

    interfaces = []
    for i, iface in enumerate(bruto["interface"]):
        interfaces.append({
            "interface": iface[""],
            "info": iface.get("info", ""),
            "IPv4": bruto["IPv4"][i][""],
            "fisico": bruto["Physical Address"][i][""],
        })
    return interfaces


def _carregar_bruto(caminho=None):
    """Le o JSON da topologia e devolve a lista de dicts crus."""
    caminho_completo = caminho or Topologia
    try:
        with open(caminho_completo, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: '{caminho_completo}' file was not found.")
        return []


def carregar_dispositivos(caminho="topologia.json"):
    """Le o arquivo de topologia e devolve {nome: Dispositivo}."""
    caminho_completo = os.path.join(_DIR_BASE, caminho) if not os.path.isabs(caminho) else caminho
    data = _carregar_bruto(caminho_completo)

    dispositivos = {}
    for bruto in data:
        nome = bruto["dispositivo"]
        interfaces = _normalizar_interfaces(bruto)
        eh_computador = isinstance(bruto["interface"], str)
        classe = Computador if eh_computador else Roteador
        dispositivos[nome] = classe(nome, interfaces)
    return dispositivos


def buscar_dispositivo(nome):
    """Usado pela camada 3 (Lay_3.encaminhar) so para checar
    alcancabilidade do destino. Devolve o dict bruto do JSON
    (nao normalizado) - suficiente para o teste 'existe ou nao
    existe' feito hoje.

    TODO (R5): quando a tabela de encaminhamento por custo for
    implementada, esta funcao (ou uma nova em rede.py) deve
    devolver tambem o proximo salto e a interface de saida,
    usando os custos da Figura 1 do enunciado (hoje ausentes
    do topologia.json).
    """
    for bruto in _carregar_bruto():
        if bruto["dispositivo"] == nome:
            return bruto
    return None
