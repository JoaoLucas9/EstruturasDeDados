"""Contém uma implementação de um grafo.

Constantes
    ORIENTADA e NAO_ORIENTADA: tipos das ligações do grafo.

Autor: João Lucas Alves Almeida Santos
Versão: 0.1 beta
"""

from tabelaHash import TabelaHash
from erros import ItemNaoEncontrado, FalhaNaOperacao
from copy import deepcopy
from math import ceil
from uteis import NAO_INFORMADO, executar, INDEFINIDO, INFINITO
from arvore import Heap, IGUAIS


def _itemNaoEncontrado():
    raise ItemNaoEncontrado


def _ligacoes(v1, v2):
    return (ligacao for adj, ligacao in v1.adjacentes_ligacoes if adj is v2)


def _ligacoesSemADistanciaInformada(v1, v2):
    return filter(lambda ligacao: 'distancia' not in ligacao, _ligacoes(v1,
                                                                        v2))


_VERTICES = lambda it: filter(lambda o:isinstance(o, _Vertice), it)


def _atualizar(dicio, d):
    dicio.update(d)
    return dicio


ORIENTADA = 'orientada'
NAO_ORIENTADA = 'não orientada'


class Grafo:
    """Estrutura de dados grafo, aceita ligações orientadas e não
    orientadas representadas por dicionários que armazenam
    quaisquer informações desejadas sobre a ligação no formato de
    chave-valor, por exemplo, id=1.

    A chave 'distancia' (sem acento) merece uma atenção especial, o grafo pode
    reconhecê-la e calcular a distância total ou determinar o menor caminho
    entre dois pontos. Ver a documentação dos métodos caminhos(self, a, b) e
    caminhosMinimos(self, a, b) para mais informações. O valor associado com a
    chave em questão deve ser um int ou float.

    """


    def __init__(self):
        self._vertices = []
        self._totalDeLigacoesOrientadas = 0
        self._totalDeLigacoesNaoOrientadas = 0


    @property
    def totalDeLigacoesOrientadas(self):
        """Quantidade de ligações orientadas."""
        return self._totalDeLigacoesOrientadas


    @property
    def totalDeLigacoesNaoOrientadas(self):
        """Quantidade de ligações não orientadas."""
        return self._totalDeLigacoesNaoOrientadas


    @property
    def totalDeLigacoes(self):
        """Quantidade de ligações orientadas + não orientadas."""
        return self._totalDeLigacoesOrientadas + \
               self._totalDeLigacoesNaoOrientadas


    @property
    def totalDeItens(self):
        """Quantidade de itens que o grafo possui."""
        return len(self._vertices)


    def inserir(self, item, b=NAO_INFORMADO, **info):
        """Insere o item no grafo.

        Se b for informado, será criada uma ligação orientada de item para b
        com as informações fornecidas.

        Parâmetros
           :param item o item que será inserido no grafo

           :param b opcional, o item (que já deve estar presente no grafo)
           para o qual item será ligado

           :param info as informações da ligação entre item e b, elas serão
           ignoradas se b não for informado

        Erros
           :exception ItemNaoEncontradoErro se b for informado mas não for
           localizado.

        """
        self._vertices.append(_Vertice(item))

        if b is not NAO_INFORMADO:
            self.ligar(item, b, **info)


    def __contains__(self, item):
        """Determina se o grafo possui o item."""
        for v in self._vertices:
            if v.item == item:
                return True

        return False


    def rotas(self, a, b):
        """Retorna todos os caminhos simples de a até b.

        Erros
           :exception ItemNaoEncontradoErro se a e/ou b não forem localizados.

        :return um conjunto de tuplas que representam as rotas de a para b.
        As tuplas por sua vez são formadas pelos itens do grafo.
        Se a = b, então serão retornados todos os laços que saem de a e
        retornam para a.
        """
        return {c['vertices'] for c in self.caminhos(a, b)}


    def _vertice(self, item, funcao=_itemNaoEncontrado):
        for vertice in self._vertices:
            if item == vertice.item:
                return vertice

        # recebe algum valor ?
        return funcao()


    def _rotas(self, a: '_Vertice', b: '_Vertice'):
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
        trilha = [a]
        caminhos = []
        visitados = TabelaHash(lambda v: id(v), self.totalDeItens)
        naoVisitados = lambda par: par[0] not in visitados or par[0] == b

        def caminhar(corrente):
            if len(trilha) > 1 and corrente is b:
                caminhos.append(deepcopy(trilha))
                return

            visitados[corrente] = corrente

            for v, info in filter(naoVisitados, corrente.adjacentes_ligacoes):
                trilha.extend((info, v))
                caminhar(v)
                del trilha[-2:]

            del visitados[corrente]
            return caminhos
        return caminhar(a)


    def caminhos(self, a, b):
        """Retorna uma lista contendo todos os caminhos simples de a para b.

        Cada caminho é representado por um 'dicio' formado pelos seguintes
        pares chave-valor.
           origem - início do caminho
           dest - destino
           vertices - tupla contendo todos vértices no caminho de a para b
           total - o total de vértices no caminho de a para b,
           equivalente a 'len(vertices)'

           trechos - os trechos que formam o caminho de a para b, exemplo,
           considere o caminho de a para rota, (a, b, rota), o pedaço do caminho
           de a para b é um trecho e de b para rota outro.
           O valor associado a esta chave é um dicio formado por pares
           tupla-dicio.
             A tupla é formada por dois vértices, V1 e V2, ela representa o
             deslocamento do primeiro para o segundo vértice.
             O dicio contém todas as informações da ligação entre V1 e V2.

             OBS.: há um único caso no qual o par trechos-dicio não estará
             disponível, se ao sair de a o primeiro vértice encontrado for
             b, contudo, todas as informações da ligação entre a e b podem
             ser acessadas bem como os valores das chaves citadas acima.

            distancia - a distância total do caminho, soma das distâncias
            de todos os trechos.
            Este valor só estará disponível se todos os trechos tiverem a
            distância informada e para evitar problemas ou
            comportamentos/resultados inesperados não informe valores
            negativos.

        Parâmetros
           :param a origem

           :param b destino, pode ser igual a a

        Erros
           :exception ItemNaoEncontradoErro se a ou b não for localizado.

        :return todos os possíveis caminhos de a para b, se não houver
        nenhum então retorna uma lista vazia.

        """
        caminhos = []

        for rota in self._rotas(self._vertice(a), self._vertice(b)):
            caminho = {'origem': a, 'dest': b, 'total':ceil(len(rota)/2),
                       'vertices':tuple(v.item for v in _VERTICES(rota))}

            # significa que possui apenas a origem e o destino e a ligação
            # que os conecta, (a, lig, b)
            if len(rota) is 3:
                caminhos.append(_atualizar(caminho, rota[1]))
            else:
                caminho['trechos'] = {(rota[i].item, rota[i +2].item):rota[i +1] for i in
                                      range(0, len(rota) - 2, 2)}

                distancia = self._calcularDistancia(caminho['trechos'].values())

                if distancia != INDEFINIDO:
                    caminho['distancia'] = distancia
                caminhos.append(caminho)

        return caminhos


    def _calcularDistancia(self, dicios):
        distancia = 0

        for dicio in dicios:
            x = dicio.get('distancia', INDEFINIDO)

            if x is INDEFINIDO:
                return INDEFINIDO
            distancia += x

        return distancia


    def incidentesEm(self, p):
        """Retorna uma tupla com todas as ligações que incidem/chegam em p.
        Se p não estiver presente no grafo será retornada uma tupla vazia.
        """
        return tuple(lig for v1, lig, v2 in self._vertices_ligacoes() if
                     v2.item == p)


    def _vertices_ligacoes(self):
        # v e a são vértices, l é a ligação de v para a
        # o método retorna todos os pares, juntamente com a ligação que os
        # une, possíveis
        return ((v, l, a) for v in self._vertices for a,
                                                      l in v.adjacentes_ligacoes)


    def incidentesDe(self, p):
        """Retorna uma tupla com todas as ligações que saem de p.

        Erros
           :exception ItemNaoEncontradoErro se o item não for localizado.
        """
        return tuple(lig for a, lig in self._vertice(p).adjacentes_ligacoes)


    def ligar(self, a, b, tipo=ORIENTADA, **info):
        """Liga a e b.

        A ligação é orientada de a para b.

        Parâmetros
           :param a um item

           :param b um item

           :param tipo o tipo da ligação, pode-se criar uma ligação não
           orientada informando a constante grafo.NAO_ORIENTADA

           :param info as informações da ligação.

        Erros
           :exception ItemNaoEncontradoErro se a ou b não for localizado.
        """
        # a orientação é determinada pela ordem dos itens
        a = self._vertice(a)
        b = self._vertice(b)

        a.ligar(b, info)
        if a is not b and tipo is NAO_ORIENTADA:
            b.ligar(a, info)

        if tipo is ORIENTADA:
            self._totalDeLigacoesOrientadas += 1
        else:
            self._totalDeLigacoesNaoOrientadas += 1


    def desligar(self, a, b, filtro=lambda lig:True):
        """Remove todas as ligações filtradas de a para b.

        Obs.: as ligações não orientadas itens também serão removidas.

        Parâmetros
           :param a um item

           :param b outro item

           :param filtro função que determina quais ligações de a para b
           serão removidas.
           Requisitos: 1) receber um parâmetro, os valores fornecidos (um por
           vez) serão as ligações de a para b.
           2) retornar true se a ligação deve ser desfeita, false caso
           contrário.
           Se o filtro não for informado então todas as ligações serão
           removidas.

        Erros
           :exception ItemNaoEncontradoErro se a ou b não for localizado.

           :exception Exception qualquer erro gerado durante a filtragem das
           ligações.

        """
        self._desligar(self._vertice(a), self._vertice(b), filtro)


    def _desligar(self, v1, v2, filtro):
        for ligacao in list(filter(filtro, self.ligacoes(v1.item, v2.item))):
            v1.remover(ligacao)

            for l in v2.ligacoes:
                if l is ligacao:
                    v2.remover(ligacao)
                    self._totalDeLigacoesNaoOrientadas -= 1
                    break
            else:
                self._totalDeLigacoesOrientadas -= 1


    def remover(self, item):
        """Remove o item do grafo e todas as ligações incidentes de/em item.

        Caso o item não seja encontrado o método retorna normalmente,
        sem gerar nenhum erro.

        Parâmetros
           :param item o item a ser removido
        """
        v = self._vertice(item, lambda :None)

        if v is None:
            return

        for v1, l, v2 in list(self._vertices_ligacoes()):
            if v2 is v or v1 is v:
                self._desligar(v1, v2, lambda l: True)
        self._vertices.remove(v)


    def ligacoes(self, a, b):
        """Retorna uma tupla contendo todas as ligações de a para b.

        Se a ou b não for localizado será retornada uma tupla vazia.
        """
        a = executar(lambda :self._vertice(a), None)
        b = executar(lambda :self._vertice(b), None)

        if a is None or b is None:
            return tuple()

        return tuple(_ligacoes(a, b))


    def caminhosMinimos(self, a, b):
        """Retorna uma lista com os menores caminhos de a para b.

        A lista retornada estará vazia se, 1) não for possível calcular a
        distância de nenhum dos caminhos que levam de a para b, ou 2) se não
        houver nenhum caminho possível.

        Se houver algum caminho para o qual não é possível calcular a
        distância, ele será ignorado.

        A lista retornada é semelhante a lista retornada pelo método
        caminhos(a, b).

        Parâmetros
           :param a origem
           :param b destino

        Erros
           :exception ItemNaoEncontradoErro se a ou b não for localizado.
        """
        caminhosMinimos = []
        distanciaMinima = INFINITO

        for caminho in self.caminhos(a, b):
            distancia = caminho.get('distancia', INFINITO)

            if distancia < distanciaMinima:
                distanciaMinima = distancia
                caminhosMinimos = [caminho]
            elif distancia == distanciaMinima and distancia is not INFINITO:
                caminhosMinimos.append(caminho)

        return caminhosMinimos


    # kruskal
    def arvoreCoberturaMinima(self):
        """Retorna um novo grafo que representa a árvore de cobertura mínima
        de self.

        O grafo deve ser conexo, não orientado e ponderado.
        Este método considera as distâncias entre os itens para determinar a
        árvore desejada, tais distâncias podem ser informadas através do
        método ligar(a, b, **info), basta informar o par 'distancia=x',
        sendo x um int ou um float, pelo 3º parâmetro.
        É possível que algumas ligações não tenham a distância informada e
        mesmo assim o método retornar normalmente, deste de que seja
        possível determinar a árvore.

        Erros
           :exception Exception se o grafo não for conexo

           :exception FalhaNaOperacao se uma das ligações não tiver a
           distância informada e impossibilitar a determinação da
           árvore de cobertura mínima, ou se o grafo possuir ligações
           orientadas.

        """
        if self.totalDeLigacoesOrientadas > 0:
            raise FalhaNaOperacao('O grafo deve ser não orientado.')

        conjuntos = [{}]
        novasLigacoes = []
        ligacoes = self._ligacoes()

        while len(conjuntos[0]) < len(self._vertices):
            l = ligacoes.remover()
            conjuntoV1 = self._conjunto(l[0], conjuntos)
            conjuntoV2 = self._conjunto(l[2], conjuntos)

            if 'distancia' not in l[1]:
                raise FalhaNaOperacao

            if conjuntoV1 is not conjuntoV2 and l[0] != l[2]:
                novasLigacoes.append(l)
                conjuntos.insert(0, conjuntoV1 + conjuntoV2)

        return self._novoGrafo(novasLigacoes)


    def _ligacoes(self):
        """Retorna uma lista de prioridades contendo dicios
        campos origem, destino e ligação"""
        ligacoes = Heap(lambda x1, x2: IGUAIS if x1 == x2 else min(x1, x2))

        for v1, lig, v2 in self._vertices_ligacoes():
            ligacoes.inserir((v1.item, lig, v2.item),
                             lig.get('distancia', INFINITO))

        return ligacoes


    def _ligacoesSemDistancia(self, a, b):
        """Retorna um gerador que itera por todas as ligações de a para b que
        não possuem a distância informada."""
        return filter(lambda ligacao: 'distancia' not in ligacao,
                      self.ligacoes(a, b))


    def _conjunto(self, item, conjuntos):
        """Retorna o conjunto do item."""
        for conjunto in conjuntos:
            if item in conjunto:
                return conjunto
        return [item]


    def _novoGrafo(self, conjunto):
        grafo = Grafo()

        for tupla in conjunto:
            origem = tupla[0]
            ligacao = tupla[1]
            destino = tupla[2]

            if origem not in grafo:
                grafo.inserir(origem)

            if destino not in grafo:
                grafo.inserir(destino)

            grafo.ligar(origem, destino, NAO_ORIENTADA, **ligacao)

        return grafo


class _Vertice:
    """Os vértices do grafo."""
    # nova estrutura: propriedade adjacentes = vertices adjacentes a este
    # precisa melhorar um pouco

    def __init__(self, item):
        self.item = item

        # adjacentes é uma lista que segue o padrão [v1, l1, v2, l2 ..., vn,
        # ln] onde v1, v2 ...vn são vértices e l1, l2 ...ln são ligações,
        # l1 é a ligação se self com v1, l2 a ligação de self com v2 e assim
        # por diante.
        self._adjacentes = []


    @property
    def adjacentes(self):
        """Iterador que percorre os vértices adjacentes a self."""
        return (e for e in self._adjacentes if isinstance(e, _Vertice))


    @property
    def adjacentes_ligacoes(self):
        """Iterador que percorre todos os vértices adjacentes a self,
        e retorna o par vértice-ligação."""
        it = iter(self._adjacentes)

        return ((vertice, next(it)) for vertice in it)


    @property
    def ligacoes(self):
        """Todas as ligações 'incidentes de' de self."""
        return (e for e in self._adjacentes if isinstance(e, dict))


    def ligar(self, vertice, ligacao=None):
        """Liga este vértice ao vértice informado.
        Exemplo: seja este o vértice A e o vértice informado é o B,
        este método ligará A e B.
        A ligação não é orientada.

        Parâmetros
           :param vertice o vértice ao qual este será interligado.

           :param dicio informações sobre a nova ligação
        """
        self._adjacentes.append(vertice)
        self._adjacentes.append(dict() if ligacao is None else ligacao)


    def remover(self, ligacao):
        i = executar(lambda :self._adjacentes.index(ligacao), -1)

        if i is not -1:
            del self._adjacentes[i - 1:i + 1]


    def desligar(self, vertice):
        i = executar(lambda :self._adjacentes.index(vertice), -1)

        while i is not -1:
            del self._adjacentes[i:i +2]
            i = executar(lambda :self._adjacentes.index(vertice), -1)


    def __repr__(self):
        return self.item



