"""Funções utilitárias para iteráveis.
Novas funções serão adicionadas em versões futuras.

Autor: João Lucas Alves Almeida Santos
Versão: 0.1
"""

from collections.abc import Sized


def tamanho(iteravel):
    """Retorna o tamanho do iterável."""
    if isinstance(iteravel, Sized):
        return len(iteravel)
    return  sum(1 for x in iteravel)


def vazio(iteravel):
    """Retorna true se o iterável estiver vazio, false caso contrário."""
    return tamanho(iteravel) is 0

