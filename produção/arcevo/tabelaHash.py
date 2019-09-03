from erros import ItemNaoEncontrado as ChaveNaoEncontrada


def _chaveNaoEncontrada(chave):
    raise ChaveNaoEncontrada(f'A chave "{chave}" não foi encontrada.')


def _codigoHash(chave: str):
    """Gera o código usando apenas os 10 primeiros caracteres da str,
    ou toda, se ela possuir menos que 10 caracteres."""
    return sum(ord(chave[i]) * (33 ** i) for i in range(min(len(chave), 10)))


class TabelaHash:


    def __init__(self, capacidade=11, fator=0.75):
        self._arranjo = [[] for i in range(capacidade)]
        self._tamanho = 0
        self._fatorDeCarga = fator


    @property
    def tamanho(self):
        """Quantidade de pares chave-valor na tabela."""
        return self._tamanho
    
    
    @property
    def fatorDeCarga(self):
        """Fator de carga atual da tabela."""
        return self.tamanho/len(self._arranjo)

    @property
    def fatorDeCargaLimite(self):
        return self._fatorDeCarga


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

        if self.fatorDeCarga > self.fatorDeCargaLimite:
            self._rehash()


    def _rehash(self):
        # descobrir a nova capacidade do arranjo
        novaCapacidade = len(self._arranjo)

        while self._tamanho/novaCapacidade >= self.fatorDeCargaLimite:
            novaCapacidade += 1

        #---------------------------------------------------------

        # criação da nova tabela
        novoArranjo = [[] for i in range(novaCapacidade)]






    def _inserirNaTabela(self, entrada, posicao):
        self._arranjo[posicao].append(entrada)


    def __contains__(self, chave):
        return self._entrada(chave, lambda c: None) is not None


    def _entrada(self, chave, funcao=_chaveNaoEncontrada):
        for entrada in self._arranjo[self._comprimir(_codigoHash(chave))]:
            if chave == entrada.chave:
                return entrada

        return funcao(chave)


    def _comprimir(self, codigo):
        # a compressão é individual para cada tabela, denpende do tamanho de
        # cada uma
        p = 37
        a = 1
        b = 13

        return ((a * codigo + b) % p) % len(self._arranjo)


    def __getitem__(self, chave):
        return self._entrada(chave).valor


class _Entrada:


    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor
