from tabelaHash import TabelaHash
from erros import ItemNaoEncontrado


def _itemNaoEncontrado():
    raise ItemNaoEncontrado


class Grafo:


    def __init__(self):
        self._vertices = []


    def ligacoes_com_informacoes(self):
        am = _Vertice('AM')
        pe = _Vertice('PE')
        rj = _Vertice('RJ')
        sp = _Vertice('SP')
        mg = _Vertice('MG')

        am.ligar(pe, distancia=2833, id='010')
        am.ligar(sp, distancia=2689, id='015')
        pe.ligar(rj, distancia=1874, id='020')
        rj.ligar(sp, distancia=357, id='025')

        pe.ligar(am, distancia=2833, id='010')
        sp.ligar(am, distancia=2689, id='015')
        rj.ligar(pe, distancia=1874, id='020')
        sp.ligar(rj, distancia=357, id='025')

        self._vertices = [am, pe, rj, sp, mg]

        return self


    def ligacoes_simples(self):
        am = _Vertice('AM')
        pe = _Vertice('PE')
        rj = _Vertice('RJ')
        sp = _Vertice('SP')
        mg = _Vertice('MG')

        am.ligar(pe)
        am.ligar(sp)
        pe.ligar(rj)
        rj.ligar(sp)

        pe.ligar(am)
        sp.ligar(am)
        rj.ligar(pe)
        sp.ligar(rj)

        self._vertices = [am, pe, rj, sp, mg]

        return self


    def caminhos(self, a, b):
        """Retorna todos os caminhos simples de a até b.

        Erros
           :exception ItemNaoEncontradoErro se a e/ou b não forem localizados.

        :return uma coleção contendo todos os caminhos de a para b, se não
        houver nenhum a coleção ficará vazia.
        Se a = b, então serão retornados todos os laços que saem de e
        retornam para a.
        """
        if a == b:
            caminhos = self._lacos(self._vertice(a))
        else:
            caminhos = self._caminhos(self._vertice(a), self._vertice(b))

        return tuple(tuple(v.item for v in caminho) for caminho in caminhos)


    def _vertice(self, item, funcao=_itemNaoEncontrado):
        for vertice in self._vertices:
            if item == vertice.item:
                return vertice

        return funcao()


    def _lacos(self, vertice):
        caminhos = list(c for v in vertice.adjacentes for c in self._caminhos(v, vertice))

        for c in (c for c in caminhos):
            c.insert(0, vertice)

        return caminhos


    def _caminhos(self, a: '_Vertice', b: '_Vertice'):
        """Retorna todos os caminhos possíveis de a até b.
        :type b: _Vertice
        :type a: _Vertice
        """
        trilha, caminhos = [], []
        visitados = TabelaHash(lambda v: id(v), 20)
        naoVisitados = lambda v: v not in visitados

        def caminhar(corrente):
            if corrente is b:
                caminhos.append(trilha.copy() + [b])
                return

            trilha.append(corrente)
            visitados[corrente] = corrente

            for v in filter(naoVisitados, corrente.adjacentes):
                caminhar(v)

            trilha.remove(corrente)
            return caminhos

        return caminhar(a)


    def trajetos(self, a, b):
        pass


class _Vertice:
    # nova estrutura: propiedade adjacentes = vertices adjacentes a este
    # precisa melhorar um pouco

    def __init__(self, item):
        self.item = item
        self._adjacentes = []


    @property
    def adjacentes(self):
        return (par['vertice'] for par in self._adjacentes)


    def ligar(self, vertice, **info):
        """Liga este vertice ao vertice informado.
        Exemplo: seja este o vertice A e o vertice informado é o B,
        este método ligará A e B.
        A ligação não é orientada.

        Parâmetros
           :param vertice o vertice ao qual este será interligado.

           :param dicio informações sobre a nova ligação
        """
        self._adjacentes.append({'vertice':vertice, 'info':info})






