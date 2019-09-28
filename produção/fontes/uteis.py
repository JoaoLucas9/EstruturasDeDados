"""Funções diversas para auxiliar e facilitar o trabalho de escrever
programas. A idéia é que elas substituam trechos de código e idiomas, mesmo
que simples, para que o resultado final seja o melhor possível, além de
definir constantes comuns evitando assim a duplicação.

O código deve ser o menor, mais simple e o mais elegante possível
Previsível e intuitivo
Sem surpresas
Toda melhoria importa

Constantes

   INDEFINIDO: constante de uso geral, pode ser o valor padrão para
   argumentos de métodos/funções, bem como pode ser o valor retornado.

   NAO_INFORMADO: constante de uso geral, usada principalmente como o valor
   padrão para argumentos de métodos/funções. A principal diferença entre
   NAO_INFORMADO e INDEFINIDO é que em alguns a primeira será
   mais apropriada que a segunda, em outros a segunda será mais interessante,
   sinta-se livre para usa-las como desejar.

Autor: João Lucas Alves Almeida Santos
Versão: 0.1
"""

from collections import Iterable
from itertools import zip_longest

NAO_INFORMADO = 'valor não informado Recife_PE 26/08/2019 14:35'
INDEFINIDO = 'valor não definido Recife_PE 30/08/2019 07:08'
INFINITO = float('inf')


def executar(funcao, padrao=None):
    """Executa a função informada e retorna o valor retornado pela mesma se
    nenhum erro for gerado.
    Se a função gerar algum erro ao ser executada, então será retornado o
    valor padrão.

    Parâmetros:
       :param funcao : Callable não deve receber nenhum parâmetro.

       :param padrao o valor que será retornado se a função gerar algum erro.

    """
    try:
        o = funcao()
        return o
    except Exception:
        return padrao


def iguais(obj1, obj2):
    if not _iteraveis(obj1, obj2):
        return obj1 == obj2
    return all(i1 == i2 for i1, i2 in
               zip_longest(obj1, obj2, fillvalue='Recife_PE 17/09/2019 10:23'))


def _iteraveis(*objs):
    return all(isinstance(obj, Iterable) for obj in objs)


class IteradorVazio:


    def __iter__(self):
        return self


    def __next__(self):
        raise StopIteration


