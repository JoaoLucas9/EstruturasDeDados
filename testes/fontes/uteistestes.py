"""Funções comumente usadas em testes, declaradas aqui para evitar
duplicação de código."""
from arvore import IGUAIS
# TODO renomear
import pickle as arqmin
import os

def maior(x1, x2):
    """Retorna o maior de dois números ou a constante arvore.IGUAIS se forem
    iguais.

    None é considerado menor que qualquer outro valor.
    """
    if x1 is None is not x2:
        return x2

    if x2 is None is not x1:
        return x1

    return IGUAIS if x1 == x2 else max(x1, x2)


def pickle(ed, arquivo):
    """Abre o arquivo no modo de escrita binária e escreve a ed nele.

    Após a escrita o arquivo será fechado.
    """
    with open(arquivo, 'w+b') as arq:
        arqmin.dump(ed, arq)


def load(arquivo):
    """Abre o arquivo no modo de leitura binária para carregar e retornar a
    estrutura contida no arquivo.

    Após a estrutura ter sido carregada o arquivo deletado.
    """
    with open(arquivo, 'r+b') as arq:
        ed = arqmin.load(arq)
    return ed


def deletar(arquivo):
    os.remove(arquivo)
