from tabelaHash import TabelaHash
from erros import ItemNaoEncontrado
from copy import deepcopy
from math import ceil


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
            caminhos = self._caminhosOriginal(self._vertice(a), self._vertice(b))

        return tuple(tuple(v.item for v in caminho) for caminho in caminhos)


    def _vertice(self, item, funcao=_itemNaoEncontrado):
        for vertice in self._vertices:
            if item == vertice.item:
                return vertice

        return funcao()


    def _lacos(self, vertice):
        caminhos = list(c for v in vertice.adjacentes for c in
                        self._caminhosOriginal(v, vertice))

        for c in (c for c in caminhos):
            c.insert(0, vertice)

        return caminhos


    def _caminhosOriginal(self, a: '_Vertice', b: '_Vertice'):
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


    def _caminhos(self, a: '_Vertice', b: '_Vertice'):
        """Retorna todos os caminhos possíveis de a até b.
        A lista mais externa é o conjunto de todos os caminhos possíveis de a
        para b, cada uma das listas internas representa um dos caminhos, as
        listas internas são compostas por _Vertices intercalados por dicios
        que representam as ligações entre os vertices, por exemplo, na lista
        [V1, D1, V2, D2, V3 ...Vn], D1 representa a ligação entre V1 e V2, D2
        a ligação entre V2 e V3 e assim por diante.
        :type b: _Vertice
        :type a: _Vertice

        :return lista retornada
        [[V1, I1, V2, I2, ..., Vn], [V1, I1, V2, I2, ..., Vn]]
        """
        trilha, caminhos = [a], []
        visitados = TabelaHash(lambda v: id(v), 20)
        naoVisitados = lambda par: par[0] not in visitados

        def caminhar(corrente):
            if corrente is b:
                caminhos.append(deepcopy(trilha))
                return

            visitados[corrente] = corrente

            for v, info in filter(naoVisitados, corrente.adjacentes_info):
                trilha.append(info)
                trilha.append(v)
                caminhar(v)
                trilha.pop()
                trilha.pop()

            return caminhos

        # a estrutura final da lista caminhos deve ser a seguinte:
        # [[V1, I1, V2, I2, ..., Vn], [V1, I1, V2, I2, ..., Vn]]
        # a lista mais externa é o conjunto de todos os caminhos possíveis
        # de a para b, cada uma das listas internas representa um dos
        # caminhos, as listas internas são compostas por _Vertices
        # intercalados por dicios que representam as ligações entre os
        # pares de vertices, por exemplo, [V1, D1, V2, D2, V3 ...Vn],
        # D1 representa a ligação entre V1 e V2, D2 a ligação entre V2 e V3
        # e assim por diante.
        return caminhar(a)


    def trajetosOriginal(self, a, b):
        a = self._vertice(a)
        b = self._vertice(b)
        caminhos = self._caminhos(a, b)
        lista = []

        # caminhos é uma lista contendo listas, e as listas internas possuem
        # a forma V1, D1, V2, D2, V3 ... Dn, Vn, sendo que os D1, D2 ... Dn
        # são dicios que representam as ligações entre os vertices V1, V2,
        # ... Vn, por exemplo D1 representa a ligação entre V1 e V2,
        # D2 a ligação entre V2 e V3 e assim por diante
        for c in caminhos:
            if len(c) is 3:
                d = c[1]
                d['origem'] = a.item
                d['dest'] = b.item
                d['total'] = 2
                d['vertices'] = (a.item, b.item)
            else:
                d = {'origem': a.item, 'dest': b.item,
                     'total': (len(c) // 2) + 1, 'vertices': tuple(
                         e.item for e in c if isinstance(e, _Vertice))}

                conexoes = []

                for i in range(0, len(c) - 2, 2):
                    origem = c[i].item
                    destino = c[i + 2].item
                    info = c[i + 1]
                    info['origem'] = origem
                    info['dest'] = destino
                    conexoes.append(info)

                d['conexoes'] = tuple(conexoes)
            lista.append(d)

        return lista


    def trajetosVersao2(self, a, b):
        lista = []
        vertice = lambda o: isinstance(o, _Vertice)

        # caminhos é uma lista contendo listas, e as listas internas possuem
        # a forma V1, D1, V2, D2, V3 ... Dn, Vn, sendo que os D1, D2 ... Dn
        # são dicios que representam as ligações entre os vertices V1, V2,
        # ... Vn, por exemplo D1 representa a ligação entre V1 e V2,
        # D2 a ligação entre V2 e V3 e assim por diante
        for c in self._caminhos(self._vertice(a), self._vertice(b)):
            d = {'origem': a, 'dest': b, 'total': (len(c) // 2) + 1,
                 'vertices': tuple(filter(vertice, c))}

            if len(c) is 3:
                d = dict(d, **c[1])
            else:
                conexoes = []

                for i in range(0, len(c) - 2, 2):
                    origem = c[i].item
                    info = c[i + 1]
                    destino = c[i + 2].item
                    info['origem'] = origem
                    info['dest'] = destino
                    conexoes.append(info)

                d['conexoes'] = tuple(conexoes)
            lista.append(d)

        return lista


    def trajetosV3(self, a, b):
        lista = []
        vertice = lambda o: isinstance(o, _Vertice)

        # caminhos é uma lista contendo listas, e as listas internas possuem
        # a forma V1, D1, V2, D2, V3 ... Dn, Vn, sendo que os D1, D2 ... Dn
        # são dicios que representam as ligações entre os vertices V1, V2,
        # ... Vn, por exemplo D1 representa a ligação entre V1 e V2,
        # D2 a ligação entre V2 e V3 e assim por diante
        for c in self._caminhos(self._vertice(a), self._vertice(b)):
            d = {'origem': a, 'dest': b, 'total': (len(c) // 2) + 1}

            if len(c) == 3:
                d = dict(d, **c[1])
                d['vertices'] = tuple(v.item for v in filter(vertice, c))
            else:
                conexoes = []
                vertices = [a]

                it = iter(c)
                v = next(it)

                for info in it:
                    info['origem'] = v.item
                    v = next(it)
                    vertices.append(v.item)
                    info['dest'] = v.item
                    conexoes.append(info)

                d['conexoes'] = tuple(conexoes)
                d['vertices'] = tuple(vertices)
            lista.append(d)

        return lista


    def trajetos(self, a, b):
        lista = []

        for c in self._caminhos(self._vertice(a), self._vertice(b)):
            trechos = dict()
            d = {'origem': a, 'dest': b, 'total':ceil(len(c)/2),
                 'vertices':tuple(v.item for v in c if isinstance(v, _Vertice))}

            if len(c) is 3:
                lista.append(dict(d, **c[1]))
            else:
                for i in range(0, len(c) - 2, 2):
                    trechos[(c[i].item, c[i +2].item)] = c[i +1]

                d['trechos'] = trechos
                lista.append(d)

        return lista




class _Vertice:
    # nova estrutura: propiedade adjacentes = vertices adjacentes a este
    # precisa melhorar um pouco

    def __init__(self, item):
        self.item = item

        # adjacentes é uma lista de tuplas, o primeiro item da tupla é o
        # vértice adjacente a self, e o segundo item são as informações da
        # conexão entre self e o outro vértice
        self._adjacentes = []


    @property
    def adjacentes(self):
        """Iterador que percorre os vértices adjacentes a self."""
        return (par[0] for par in self._adjacentes)


    @property
    def adjacentes_info(self):
        return (par for par in self._adjacentes)


    def ligar(self, vertice, **info):
        """Liga este vertice ao vertice informado.
        Exemplo: seja este o vertice A e o vertice informado é o B,
        este método ligará A e B.
        A ligação não é orientada.

        Parâmetros
           :param vertice o vertice ao qual este será interligado.

           :param dicio informações sobre a nova ligação
        """
        # todo acho que dá para substituir a tupla por algum objeto que possui
        # dois atributos, vértice e info, pode ser um objeto par por exemplo
        self._adjacentes.append((vertice, info))


    def __repr__(self):
        return self.item






