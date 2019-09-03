from erros import ItemNaoEncontrado as ChaveNaoEncontrada
from random import randint
from numeros import primos, primeiroPrimoMaiorQue
from itertools import chain


def _chaveNaoEncontrada(chave):
    raise ChaveNaoEncontrada(f'A chave "{chave}" não foi encontrada.')


def _codigoHash(chave: str):
    """Gera o código usando apenas os 10 primeiros caracteres da str,
    ou toda, se ela possuir menos que 10 caracteres."""
    return sum(ord(chave[i]) * (33 ** i) for i in range(min(len(chave), 10)))


class TabelaHash:


    def __init__(self, capacidade=11, fator=0.75):
        self._tabela = [[] for i in range(capacidade)]
        self._tamanho = 0
        self._fatorDeCargaMaximo = fator
        self._rehashsExecutados = 0

        p = primeiroPrimoMaiorQue(capacidade)
        self._comprimir = self._funcaoCompressao(
            randint(1, p -1), randint(0, p -1), p)


    @property
    def tamanho(self):
        """Quantidade de pares chave-valor na tabela."""
        return self._tamanho
    
    
    @property
    def fatorDeCarga(self):
        """Fator de carga atual da tabela."""
        return self.tamanho/len(self._tabela)

    @property
    def limiteFatorDeCarga(self):
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
        return self._rehashsExecutados


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
            self._inserirNaTabela(entrada, self._comprimir(_codigoHash(chave)))
        else:
            entrada.valor = valor

        self._tamanho += 1

        if self.fatorDeCarga > self.limiteFatorDeCarga:
            self._rehash()
            self._rehashsExecutados += 1


    def _rehash(self):
        tabela = self._tabela
        self._criarNovaTabela()
        self._configurarNovaFuncaoDeCompressao()
        self._copiarEntradas(tabela, self._tabela)


    def _criarNovaTabela(self):
        capacidade = primeiroPrimoMaiorQue(len(self._tabela) * 2)

        while self._tamanho/capacidade >= self.limiteFatorDeCarga:
            capacidade = primeiroPrimoMaiorQue(capacidade)

        self._tabela = [[] for i in range(capacidade)]


    def _configurarNovaFuncaoDeCompressao(self):
        p = primos[primos.index(len(self._tabela)) +1]
        self._comprimir = self._funcaoCompressao(randint(1, p - 1),
                                                 randint(0, p - 1), p)


    def _copiarEntradas(self, tabela, destino):
        for entrada in (entrada for lista in tabela for entrada in lista):
            posicao = self._comprimir(_codigoHash(entrada.chave))
            destino[posicao].append(entrada)


    def _inserirNaTabela(self, entrada, posicao):
        self._tabela[posicao].append(entrada)


    def __contains__(self, chave):
        return self._entrada(chave, lambda c: None) is not None


    def _entrada(self, chave, funcao=_chaveNaoEncontrada):
        loca = self._comprimir(_codigoHash(chave))
        # print('procurar em', loca)
        # print(self._comprimir)
        for entrada in self._tabela[loca]:
            if chave == entrada.chave:
                return entrada

        return funcao(chave)


    def _funcaoCompressao(self, a, b, p):
        # a compressão é individual para cada tabela, denpende do tamanho de
        # cada uma
        def comprimir(codigo):
            return ((a * codigo + b) % p) % len(self._tabela)

        return comprimir


    def __getitem__(self, chave):
        """Retorna o valor associado a chave."""
        return self._entrada(chave).valor


    def __iter__(self):
        return (entrada.chave for entrada in self.pares())


    def pares(self):
        return chain(entrada for lista in self._tabela for entrada in lista)


    def valores(self):
        return (entrada.valor for entrada in self.pares())


class _Entrada:


    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor
