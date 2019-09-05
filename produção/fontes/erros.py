"""Erros comuns que podem ser gerados ao trabalhar com coleções.

Autor: João Lucas Alves Almeida Santos
Versão: 0.1
"""

class FalhaNaOperacao(Exception):
    """Propósito: indicar que um método ou função falhou, exemplo:
    abrirArquivo('músicas'), suponha que o arquivo não existe, pode-se dizer
    que a operação falhou e 'abrirArquivo' poderia gerar uma
    FalhaNaOperacao."""
    pass


class ItemNaoEncontrado(FalhaNaOperacao):
    """Propósito: criada para ser utilizada com coleções, este erro indica
    que um item não pôde ser localizado.

    Exemplo: seja C uma coleção e M um método de C que executa uma operação
    sobre um dos itens de C, agora considere o código: C.M(x), se x estiver
    em C e puder ser encontrado então a operação será executada normalmente,
    contudo se x não puder ser localizado em C então M poderia gerar um
    ItemNaoEncontrado.
    """
    def __init__(self, item=None):
        m = f'{"Item" if item is None else item} não encontrado.'
        super().__init__(m)


class ParametroNaoInformado(FalhaNaOperacao):
    """Propósito: indicar que um parâmetro não foi informado na chamada de
    um método ou função.

    Exemplo: seja F uma função que declara 1 argumento obrigatório X e 1
    opcional Y, temos portanto F(X, [y]), considere que se o 1º parâmetro
    informado for P então o opcional Y também deve ser informado,
    se a função for chamada F(P) (com o 2º parâmetro faltando), F poderia
    então disparar um ParametroNaoInformado.

    Generalizando: um erro deste tipo pode ser disparado quando uma função
    ou um método for chamado com um ou mais parâmetros faltando.
    """
    def __init__(self, param):
        super().__init__(f'O parâmetro "{param}" não foi especificado.')


class ColecaoVazia(FalhaNaOperacao):
    """Erro gerado ao tentar executar uma operação, como remover um item de
    uma pilha ou acessar o último item de uma lista, sobre uma coleção vazia.
    """

