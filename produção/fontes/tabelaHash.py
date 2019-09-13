"""Implementação de uma TabelaHash.

Autor: João Lucas Alves Almeida Santos
Versão: 0.1 beta
"""

from erros import ItemNaoEncontrado as ChaveNaoEncontrada
from random import randint
from numeros import primos, primeiroPrimoMaiorQue
from itertools import chain


def _chaveNaoEncontrada(chave):
    raise ChaveNaoEncontrada(f'A chave "{chave}" não foi encontrada.')


class TabelaHash:
    """Implementação de um mapa.

    Utiliza encadeamento separado para tratar colisões."""


    def __init__(self, funcaoHash, capacidade=11, fatorDeCargaMaximo=0.75):
        """
        Parâmetros
           :param funcaoHash a função que irá gerar os códigos hash das chaves.
           Os valores podem ser negativos.

           :param capacidade a capacidade inicial da tabela.
           Valor padrão: 11

           :param fatorDeCargaMaximo o limite para o fator de carga,
           caso este limite seja ultrapassado então executa-se o rehash.
           Valor padrão: 0.75
        """
        self._tabela = [[] for i in range(capacidade)]
        self._tamanho = 0
        self._fatorDeCargaMaximo = fatorDeCargaMaximo
        self._rehashsExecutados = 0
        self._codigoHash = funcaoHash
        self._totalDeColisoes = 0

        p = primeiroPrimoMaiorQue(capacidade)
        self._comprimir = self._funcaoCompressao(
            randint(1, p -1), randint(0, p -1), p)


    @property
    def tamanho(self):
        """Quantidade de pares chave-valor na tabela.
        Escrita: ✗
        """
        return self._tamanho
    
    
    @property
    def fatorDeCarga(self):
        """Fator de carga atual da tabela.
        Escrita: ✗
        """
        return self.tamanho/len(self._tabela)

    @property
    def limiteFatorDeCarga(self):
        """O limite para o fator de carga.
        Escrita: ✓
        Deve ser maior que zero.
        """
        return self._fatorDeCargaMaximo


    @limiteFatorDeCarga.setter
    def limiteFatorDeCarga(self, y):
        if y <= 0:
            raise AttributeError('O valor informado deve ser maior que zero.')

        self._fatorDeCargaMaximo = y

        if self.fatorDeCarga > y:
            self._rehash()


    @property
    def rehashsExecutados(self):
        """Quantidade de rehash executados.
        Escrita: ✗
        """
        return self._rehashsExecutados


    @property
    def totalDeColisoes(self):
        """Total de colisões que ocorreram durante as inserções dos pares
        chave-valor na tabela.
        As colisões que ocorrem durante o rehash não são computadas.
        Substituir o valor associado a uma chave também não altera o total
        de colisões.
        Escrita: ✗
        """
        return self._totalDeColisoes


    @property
    def vazia(self):
        """True se o heap estiver vazio, false caso contrário.
        Escrita: ✗
        """
        return self.tamanho is 0


    def __setitem__(self, chave, valor):
        """Insere o par chave-valor ou substitui o atual
        valor da chave (se ela já estiver presente na tabela).


        Parâmetros:
           :param chave uma chave

           :param valor
           1) não é um callable: simplesmente insere-se a chave juntamente
           com o valor na tabela.

           2) é um callable: informa-se a chave e o seu valor atual para o
           callable (nesta ordem), o valor retornado da função será inserido
           juntamente com a chave, ou o atual valor da chave será substituido.
           Se a chave ainda não estiver na tabela, então None será informado
           como o valor.
        """
        entrada = self._entrada(chave, lambda ign: None)

        if callable(valor):
            valor = valor(chave, getattr(entrada, 'valor', None))

        if entrada is None:
            entrada = _Entrada(chave, valor)
            posicao = self._comprimir(self._codigoHash(chave))
            self._inserirNaTabela(entrada, posicao)
        else:
            entrada.valor = valor

        self._tamanho += 1

        if self.fatorDeCarga > self.limiteFatorDeCarga:
            self._rehash()
            self._rehashsExecutados += 1


    def _rehash(self):
        tabela = self._tabela
        self._criarNovaTabela()
        self._configurarNovaFuncaoCompressao()
        self._copiarEntradas(tabela, self._tabela)


    def _criarNovaTabela(self):
        capacidade = primeiroPrimoMaiorQue(len(self._tabela) * 2)

        while self._tamanho/capacidade >= self.limiteFatorDeCarga:
            capacidade = primeiroPrimoMaiorQue(capacidade)

        self._tabela = [[] for i in range(capacidade)]


    def _configurarNovaFuncaoCompressao(self):
        p = primos[primos.index(len(self._tabela)) +1]
        self._comprimir = self._funcaoCompressao(randint(1, p - 1),
                                                 randint(0, p - 1), p)


    def _copiarEntradas(self, tabela, destino):
        for entrada in (entrada for lista in tabela for entrada in lista):
            posicao = self._comprimir(self._codigoHash(entrada.chave))
            destino[posicao].append(entrada)


    def _inserirNaTabela(self, entrada, posicao):
        lista = self._tabela[posicao]

        if len(lista) > 0:
            self._totalDeColisoes += 1

        lista.append(entrada)


    def __contains__(self, chave):
        """Determina se a chave está na tabela.

        :return true se a chave for localizada na tabela, false caso contrário.
        """
        return self._entrada(chave, lambda c: None) is not None


    def _entrada(self, chave, funcao=_chaveNaoEncontrada):
        for entrada in self._tabela[self._comprimir(self._codigoHash(chave))]:
            if chave == entrada.chave:
                return entrada

        return funcao(chave)


    def _funcaoCompressao(self, a, b, p):
        def comprimir(codigo):
            return ((a * codigo + b) % p) % len(self._tabela)

        return comprimir


    def __getitem__(self, chave):
        """Retorna o valor associado a chave.

        Erros
           :exception ItemNaoEncontrado se a chave não for localizada
        """
        return self._entrada(chave).valor


    def __iter__(self):
        """Retorna um iterador que percorre as chaves da tabela."""
        return (entrada.chave for entrada in self.pares())


    def pares(self):
        """Retorna um iterador que percorre os pares da tabela.
        Seja p um dos pares da tabela, para obter a chave basta fazer
        p.chave, analogamente, para obter o valor basta fazer p.valor.
        """
        return chain(entrada for lista in self._tabela for entrada in lista)


    def valores(self):
        """Retorna um iterador que percorre os valores da tabela."""
        return (entrada.valor for entrada in self.pares())


    def __delitem__(self, chave):
        """Remove o par que possui a chave informada.

        Erro
           :exception ItemNaoEncontrado se a chave não for localizada
        """
        lista = self._tabela[self._comprimir(self._codigoHash(chave))]
        lista.remove(self._entrada(chave))
        self._tamanho -= 1


class _Entrada:


    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor
