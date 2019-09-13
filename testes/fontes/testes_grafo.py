from grafo import Grafo, NAO_ORIENTADA
from iteruteis import vazio
from pytest import raises
from erros import ItemNaoEncontrado, FalhaNaOperacao
from pyext import naoGeraErro

#não foram realizados testes com itens duplicados
def grafoParaTestesDoMetodo_desligar():
    grafo = novoGrafo('PE', 'RJ')
    grafo.ligar('PE', 'RJ', NAO_ORIENTADA, nome='BR101', comp=1.4, ano=53)
    grafo.ligar('RJ', 'PE', nome='BR101', comp=2.5, ano=55)
    grafo.ligar('RJ', 'PE', nome='BR105', comp=2.1, ano=60)
    grafo.ligar('RJ', 'PE', NAO_ORIENTADA)
    grafo.ligar('RJ', 'RJ', origem='RJ', destino='RJ')
    grafo.ligar('RJ', 'PE')
    grafo.ligar('RJ', 'RJ', NAO_ORIENTADA, nome='retorno')

    return grafo


def contemApenas(itens, colecao: 'list ou tupla'):
    """Retorna true se todos os itens de itens forem encontrados em colecao"""
    #duplicados não serão considerados no momento em que se escreve a função
    if len(itens) != len(colecao):
        return False

    for item in itens:
        if item not in colecao:
            return False
    return True


pe_am = {'distancia':2833, 'id':'010'}
sp_pe = {'distancia':2128, 'id':'025'}
rn_mt = {'distancia':2524, 'id':'035'}
pb_rn1 = {'distancia':245, 'id':'145', 'rota':'rodoviaria'}
am_am = {'distancia': 300, 'nome': 'Retorno'}
sp_rj_sp = {'distancia':357, 'id':'030'}
pe_rj = {'distancia':1874, 'id':'020'}
mt_rn1 = {'distancia':2524, 'nome':'035'}
mt_rn2 = {'distancia':3555, 'id':'135', 'rota':'rodovia'}
mt_rn3 = {'distancia':3217, 'id':'235', 'rota':'trem'}
rn_pb_rn = {'distancia':151, 'id':'040'}
rn_pb = {'distancia':230, 'id':'140', 'rota':'rodoviaria'}
pb_rn2 = {'distancia':200, 'id':'045'}
pe_mt_pe = {'distancia': 2452, 'id': '045'}
pe_rn = {'distancia':253, 'id':'050'}
pb_pe = {'distancia':104, 'id':'055'}


def grafoDeTestes():
    estados = Grafo()
    estados.inserir('AM')
    estados.inserir('PE', 'AM', **pe_am)
    estados.inserir('SP', 'PE', **sp_pe)
    estados.inserir('RJ')
    estados.inserir('MT')
    estados.inserir('RN', 'MT', **rn_mt)
    estados.inserir('PB', 'RN', **pb_rn1)
    estados.inserir('KW')

    estados.ligar('AM', 'AM', **am_am)
    estados.ligar('SP', 'RJ', NAO_ORIENTADA, **sp_rj_sp)
    estados.ligar('PE', 'RJ', **pe_rj)
    estados.ligar('MT', 'RN', **mt_rn1)
    estados.ligar('MT', 'RN', **mt_rn2)
    estados.ligar('MT', 'RN', **mt_rn3)
    estados.ligar('RN', 'PB', NAO_ORIENTADA, **rn_pb_rn)
    estados.ligar('RN', 'PB', **rn_pb)
    estados.ligar('PB', 'RN', **pb_rn2)
    estados.ligar('PE', 'MT', NAO_ORIENTADA, **pe_mt_pe)
    estados.ligar('PE', 'RN', **pe_rn)
    estados.ligar('PB', 'PE', **pb_pe)

    return estados


def novoGrafo(*itens):
    g = Grafo()

    for item in itens:
        g.inserir(item)

    return g


grafo = grafoDeTestes()


def testes_inserir():
    grafo = Grafo()
    grafo.inserir('AM')
    grafo.inserir('PE', 'AM', **pe_am)

    assert grafo.incidentesDe('PE') == grafo.incidentesEm('AM') == (pe_am, )
    assert vazio(grafo.incidentesDe('AM'))
    assert vazio(grafo.incidentesEm('PE'))

    grafo.inserir('SP', 'PE')

    assert grafo.incidentesEm('PE') == grafo.incidentesDe('SP') == ({}, )
    assert vazio(grafo.incidentesEm('SP'))


def testes_inserir_iraGerarUmErroSeBNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        grafo.inserir('CE', '-')


def testes_inserir_iraIgnorarOTerceiroParametroSeBNaoForInformado():
    grafo = Grafo()
    grafo.inserir('PE', id=5, nome='BR101')
    grafo.inserir('AM', id=5, nome='BR101')
    grafo.inserir('SP', id=5, nome='BR101')
    grafo.inserir('RJ', id=5, nome='BR101')

    assert vazio(grafo.incidentesEm('PE'))
    assert vazio(grafo.incidentesDe('PE'))
    assert vazio(grafo.incidentesEm('AM'))
    assert vazio(grafo.incidentesDe('AM'))
    assert vazio(grafo.incidentesEm('SP'))
    assert vazio(grafo.incidentesDe('SP'))
    assert vazio(grafo.incidentesEm('RJ'))
    assert vazio(grafo.incidentesDe('RJ'))


def testes_rotas():
    assert grafo.rotas('PE', 'AM') == {('PE', 'AM')}

    caminhos = grafo.rotas('SP', 'RJ')

    assert len(caminhos) is 2
    assert ('SP', 'RJ') in caminhos
    assert ('SP', 'PE', 'RJ') in caminhos

    caminhos = grafo.rotas('RN', 'PE')

    assert len(caminhos) is 2
    assert ('RN', 'MT', 'PE') in caminhos
    assert ('RN', 'PB', 'PE') in caminhos


def testes_oOperador_in_determinaSeOGrafoPossuiUmItem():
    assert 'MT' in grafo
    assert 'RN' in grafo

    assert '-' not in grafo


def testes_rotas_retornaUmConjuntoVazioSeNaoHouverCaminhoDeAParaB():
    assert vazio(grafo.rotas('AM', 'SP'))


def testes_rotas_iraGerarUmErroSeANaoForLocalizado():
    with raises(ItemNaoEncontrado):
        grafo.rotas('-', 'PE')


def testes_rotas_iraGerarUmErroSeBNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        grafo.rotas('PE', '-')


def testes_rotas_retornaraTodosOsLacosSeAeBForemOsMesmos():
    caminhos = grafo.rotas('SP', 'SP')

    assert  len(caminhos) is 2
    assert ('SP', 'RJ', 'SP') in caminhos
    assert ('SP', 'PE', 'RJ', 'SP') in caminhos

    assert grafo.rotas('AM', 'AM') == {('AM', 'AM')}


def testes_caminhos():
    assert grafo.caminhos('PE', 'AM') == [{'origem': 'PE', 'dest': 'AM',
                                          'distancia':2833, 'id':'010',
                                          'total':2, 'vertices':('PE', 'AM')}]

    trajetos = grafo.caminhos('SP', 'RJ')

    assert len(trajetos) is 2

    assert {'origem':'SP', 'dest':'RJ', 'distancia':357, 'id':'030',
    'total':2, 'vertices':('SP', 'RJ')} in trajetos

    assert {'origem':'SP', 'dest':'RJ', 'total':3,
            'vertices':('SP', 'PE', 'RJ'), 'distancia':4002,
            'trechos':{('SP', 'PE'): {'distancia':2128, 'id':'025'},
                       ('PE', 'RJ'): {'distancia':1874, 'id':'020'}}
            } in trajetos


    trajetos = grafo.caminhos('MT', 'RN')
    assert len(trajetos) is 4

    assert {'origem':'MT', 'dest':'RN', 'distancia':2524, 'nome':'035',
            'total':2, 'vertices':('MT', 'RN')} in trajetos

    assert {'origem':'MT', 'dest':'RN', 'distancia':3555, 'id':'135',
            'total':2, 'vertices':('MT', 'RN'), 'rota':'rodovia'} in trajetos

    assert {'origem':'MT', 'dest':'RN', 'distancia':3217, 'id':'235',
            'total':2, 'vertices':('MT', 'RN'), 'rota':'trem'} in trajetos

    assert {'origem':'MT', 'dest':'RN', 'total':3,
            'vertices':('MT', 'PE', 'RN'), 'distancia':2705,
            'trechos':{('MT', 'PE'):{'distancia': 2452, 'id': '045'},
                       ('PE', 'RN'):{'distancia':253, 'id':'050'}
                       }} in trajetos


def testes_caminhos_comA_igualA_B():
    # am está ligado a ele mesmo, há um laço self, está se testando o
    # código com um laço self
    assert grafo.caminhos('AM', 'AM') == [{'origem': 'AM', 'dest': 'AM',
                                           'vertices':('AM', 'AM'), 'total':2,
                                            'distancia':300, 'nome':'Retorno'}]

    trajetos = grafo.caminhos('RJ', 'RJ')

    assert len(trajetos) is 2
    assert {'origem':'RJ', 'dest':'RJ', 'total':3,
            'vertices':('RJ', 'SP', 'RJ'), 'distancia':714,
            'trechos':{('RJ', 'SP'):{'distancia':357, 'id':'030'},
                       ('SP', 'RJ'):{'distancia':357, 'id':'030'}}} in trajetos

    assert {'origem':'RJ', 'dest':'RJ', 'total':4,
            'vertices':('RJ', 'SP', 'PE', 'RJ'), 'distancia':4359,
            'trechos':{('RJ', 'SP'):{'distancia':357, 'id':'030'},
                       ('SP', 'PE'):{'distancia':2128, 'id':'025'},
                       ('PE', 'RJ'):{'distancia':1874, 'id':'020'}}} in trajetos


def testes_caminhos_iraGerarUmErroSeANaoForLocalizado():
    with raises(ItemNaoEncontrado):
        grafo.caminhos('-', 'PE')


def testes_caminhos_iraGerarUmErroSeBNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        grafo.caminhos('PE', '-')


def testes_caminhos_retornaUmaListaVaziaSeNaoHouverCaminhoDeAParaB():
    assert vazio(grafo.caminhos('AM', 'PE'))


def testes_caminhos_naoEPossivelDeterminarADistanciaEntreAeB():
    grafo = novoGrafo('PE', 'MT', 'RN', 'PB')
    grafo.ligar('PE', 'MT', distancia=2452, id='010')
    grafo.ligar('MT', 'RN', distancia=2524, id='035')
    grafo.ligar('MT', 'RN', id='135')
    grafo.ligar('MT', 'RN', distancia=3217, id='235')
    grafo.ligar('MT', 'RN', id='335')
    grafo.ligar('PE', 'RN', distancia=253, id='050')
    grafo.ligar('RN', 'PB', NAO_ORIENTADA, distancia=151, id='040')
    grafo.ligar('RN', 'PB', id='140')

    caminhos = grafo.caminhos('PE', 'RN')
    assert len(caminhos) is 5
    assert {'origem':'PE', 'dest':'RN', 'total':3, 'distancia':4976,
            'vertices':('PE', 'MT', 'RN'),
            'trechos':{('PE', 'MT'):{'distancia':2452, 'id':'010'},
                       ('MT', 'RN'):{'distancia':2524, 'id':'035'}}} in\
           caminhos

    assert {'origem':'PE', 'dest':'RN', 'total':3,
            'vertices':('PE', 'MT', 'RN'),
            'trechos':{('PE', 'MT'):{'distancia':2452, 'id':'010'},
                       ('MT', 'RN'):{'id':'135'}}} in caminhos

    assert {'origem':'PE', 'dest':'RN', 'total':3, 'distancia':5669,
            'vertices':('PE', 'MT', 'RN'),
            'trechos':{('PE', 'MT'):{'distancia':2452, 'id':'010'},
                       ('MT', 'RN'):{'distancia':3217, 'id':'235'}}} in\
           caminhos

    assert {'origem':'PE', 'dest':'RN', 'total':3,
            'vertices':('PE', 'MT', 'RN'),
            'trechos':{('PE', 'MT'):{'distancia':2452, 'id':'010'},
                       ('MT', 'RN'):{'id':'335'}}} in caminhos

    caminhos = grafo.caminhos('MT', 'PB')

    assert len(caminhos) is 8
    assert {'origem':'MT', 'dest':'PB', 'total':3, 'distancia':2675,
            'vertices':('MT', 'RN', 'PB'),
            'trechos':{('MT', 'RN'):{'distancia':2524, 'id':'035'},
                       ('RN', 'PB'):{'distancia':151, 'id':'040'}}} in caminhos

    assert {'origem':'MT', 'dest':'PB', 'total':3,
            'vertices':('MT', 'RN', 'PB'),
            'trechos':{('MT', 'RN'):{'distancia':2524, 'id':'035'},
                       ('RN', 'PB'):{'id':'140'}}} in caminhos

    assert {'origem':'MT', 'dest':'PB', 'total':3,
            'vertices':('MT', 'RN', 'PB'),
            'trechos':{('MT', 'RN'):{'id':'135'},
                       ('RN', 'PB'):{'distancia':151, 'id':'040'}}} in caminhos

    assert {'origem':'MT', 'dest':'PB', 'total':3,
            'vertices':('MT', 'RN', 'PB'),
            'trechos':{('MT', 'RN'):{'id':'135'},
                       ('RN', 'PB'):{'id':'140'}}} in caminhos

    assert {'origem':'MT', 'dest':'PB', 'total':3, 'distancia':3368,
            'vertices':('MT', 'RN', 'PB'),
            'trechos':{('MT', 'RN'):{'distancia':3217, 'id':'235'},
                       ('RN', 'PB'):{'distancia':151, 'id':'040'}}} in caminhos

    assert {'origem':'MT', 'dest':'PB', 'total':3,
            'vertices':('MT', 'RN', 'PB'),
            'trechos':{('MT', 'RN'):{'distancia':3217, 'id':'235'},
                       ('RN', 'PB'):{'id':'140'}}} in caminhos


def testes_incidentesEm():
    assert contemApenas((am_am, pe_am), grafo.incidentesEm('AM'))
    assert contemApenas((pe_mt_pe, sp_pe, pb_pe), grafo.incidentesEm('PE'))


def testes_incidentesEm_retornaUmaTuplaVaziaSeOItemNaoForLocalizado():
    assert vazio(grafo.incidentesEm('-'))


def testes_incidentesEm_comUmItemQueNaoPossuiNenhumaLigacaoIncidente():
    assert vazio(grafo.incidentesEm('KW'))


def testes_incidentesDe():
    ligacoes = grafo.incidentesDe('MT')
    assert contemApenas((mt_rn1, mt_rn2, mt_rn3, pe_mt_pe), ligacoes)

    assert contemApenas((am_am, ), grafo.incidentesDe('AM'))

    ligacoes = grafo.incidentesDe('PB')
    assert contemApenas((rn_pb_rn, pb_rn1, pb_rn2, pb_pe), ligacoes)


def testes_incidentesDe_geraUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        grafo.incidentesDe('-')


def testes_incidentesDe_comUmItemQueNaoPossuiNenhumaLigacaoIncidente():
    assert vazio(grafo.incidentesDe('KW'))


def testes_ligar():
    # 1 ligação de a para b
    # 2 ligações de b para a sem informações
    # 2 ligações de b para a com informações
    # 4 ligações orientedas
    # 2 ligações não orientedas
    # 1 laço self em b
    # total de ligações: 6
    grafo = novoGrafo('PE', 'RJ')

    grafo.ligar('PE', 'RJ', NAO_ORIENTADA, nome='BR101', comp=1.4, ano=53)

    assert grafo.incidentesEm('RJ') == grafo.incidentesDe('PE') == \
           grafo.incidentesEm('PE') == grafo.incidentesDe('RJ') == \
           ({'nome':'BR101', 'comp':1.4, 'ano':53}, )

    grafo.ligar('RJ', 'PE', nome='BR101', comp=2.5, ano=55)

    incidentesEmPE = grafo.incidentesEm('PE')
    incidentesDeRJ = grafo.incidentesDe('RJ')

    assert len(incidentesEmPE) == len(incidentesDeRJ) == 2
    assert grafo.incidentesDe('PE') == grafo.incidentesEm('RJ') == \
           ({'nome':'BR101', 'comp':1.4, 'ano':53}, )

    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesEmPE
    assert {'nome':'BR101', 'comp':2.5, 'ano':55} in incidentesEmPE
    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesDeRJ
    assert {'nome':'BR101', 'comp':2.5, 'ano':55} in incidentesDeRJ


    grafo.ligar('RJ', 'PE', nome='BR105', comp=2.1, ano=60)

    incidentesEmPE = grafo.incidentesEm('PE')
    incidentesDeRJ = grafo.incidentesDe('RJ')

    assert grafo.incidentesDe('PE') == grafo.incidentesEm('RJ') == \
           ({'nome':'BR101', 'comp':1.4, 'ano':53}, )

    assert len(incidentesEmPE) == len(incidentesDeRJ) == 3
    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesEmPE
    assert {'nome':'BR101', 'comp':2.5, 'ano':55} in incidentesEmPE
    assert {'nome':'BR105', 'comp':2.1, 'ano':60} in incidentesEmPE
    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesDeRJ
    assert {'nome':'BR101', 'comp':2.5, 'ano':55} in incidentesDeRJ
    assert {'nome':'BR105', 'comp':2.1, 'ano':60} in incidentesDeRJ


    grafo.ligar('RJ', 'PE', NAO_ORIENTADA)

    incidentesEmPE = grafo.incidentesEm('PE')
    incidentesDePE = grafo.incidentesDe('PE')
    incidentesEmRJ = grafo.incidentesEm('RJ')
    incidentesDeRJ = grafo.incidentesDe('RJ')

    assert len(incidentesEmPE) == len(incidentesDeRJ) == 4
    assert len(incidentesDePE) == len(incidentesEmRJ) == 2
    assert {} in incidentesDePE
    assert {} in incidentesEmRJ

    grafo.ligar('RJ', 'RJ', origem='RJ', destino='RJ')

    incidentesEmRJ = grafo.incidentesEm('RJ')
    incidentesDeRJ = grafo.incidentesDe('RJ')

    assert len(incidentesDeRJ) == 5
    assert len(incidentesEmRJ) == 3

    assert {'origem':'RJ', 'destino':'RJ'} in incidentesEmRJ
    assert {'origem':'RJ', 'destino':'RJ'} in incidentesDeRJ

    grafo.ligar('RJ', 'PE')

    incidentesEmPE = grafo.incidentesEm('PE')
    incidentesDePE = grafo.incidentesDe('PE')
    incidentesEmRJ = grafo.incidentesEm('RJ')
    incidentesDeRJ = grafo.incidentesDe('RJ')

    assert len(incidentesEmPE) is 5
    assert len(incidentesDePE) is 2
    assert len(incidentesDeRJ) is 6
    assert len(incidentesEmRJ) is 3

    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesDePE
    assert {} in incidentesDePE
    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesEmPE
    assert {'nome':'BR101', 'comp':2.5, 'ano':55} in incidentesEmPE
    assert {'nome':'BR105', 'comp':2.1, 'ano':60} in incidentesEmPE
    assert incidentesEmPE.count({}) == 2
    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesDeRJ
    assert {'nome':'BR101', 'comp':2.5, 'ano':55} in incidentesDeRJ
    assert {'nome':'BR105', 'comp':2.1, 'ano':60} in incidentesDeRJ
    assert {'origem':'RJ', 'destino':'RJ'} in incidentesDeRJ
    assert incidentesDeRJ.count({}) == 2
    assert {'origem':'RJ', 'destino':'RJ'} in incidentesEmRJ
    assert {} in incidentesEmRJ
    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesEmRJ

    grafo.ligar('RJ', 'RJ', NAO_ORIENTADA, nome='retorno')

    incidentesEmRJ = grafo.incidentesEm('RJ')
    incidentesDeRJ = grafo.incidentesDe('RJ')

    assert len(incidentesDeRJ) is 7
    assert len(incidentesEmRJ) is 4
    assert incidentesEmRJ.count({'nome':'retorno'}) == 1
    assert incidentesDeRJ.count({'nome':'retorno'}) == 1


def testes_ligar_geraUmErroSeUmDosItensNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        grafo.ligar('-', 'PE')

    with raises(ItemNaoEncontrado):
        grafo.ligar('PE', '-')


def testes_totalDeLigacoesOrientadas_e_NaoOrientadas_aposLigarAlgunsVertices():
    grafo = novoGrafo('AM', 'PE', 'RJ', 'SP')
    grafo.ligar('PE', 'RJ', NAO_ORIENTADA)

    assert grafo.totalDeLigacoesOrientadas is 0
    assert grafo.totalDeLigacoesNaoOrientadas is 1

    grafo.ligar('RJ', 'PE')
    grafo.ligar('RJ', 'PE')

    assert grafo.totalDeLigacoesOrientadas is 2
    assert grafo.totalDeLigacoesNaoOrientadas is 1

    grafo.ligar('SP', 'PE')
    grafo.ligar('PE', 'AM', NAO_ORIENTADA)
    grafo.ligar('SP', 'AM')

    assert grafo.totalDeLigacoesOrientadas is 4
    assert grafo.totalDeLigacoesNaoOrientadas is 2

    grafo.ligar('PE', 'AM', NAO_ORIENTADA)
    grafo.ligar('PE', 'AM', NAO_ORIENTADA)

    assert grafo.totalDeLigacoesOrientadas is 4
    assert grafo.totalDeLigacoesNaoOrientadas is 4


def testes_desligar():
    grafo = grafoParaTestesDoMetodo_desligar()
    grafo.desligar('PE', 'RJ', lambda lig: lig == {})

    incidentesEmPE = grafo.incidentesEm('PE')
    incidentesDePE = grafo.incidentesDe('PE')
    incidentesEmRJ = grafo.incidentesEm('RJ')
    incidentesDeRJ = grafo.incidentesDe('RJ')

    assert len(incidentesEmPE) is 4
    assert len(incidentesDePE) is 1
    assert len(incidentesDeRJ) is 6
    assert len(incidentesEmRJ) is 3

    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesDePE
    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesEmPE
    assert {'nome':'BR101', 'comp':2.5, 'ano':55} in incidentesEmPE
    assert {'nome':'BR105', 'comp':2.1, 'ano':60} in incidentesEmPE
    assert {} in incidentesEmPE
    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesDeRJ
    assert {'nome':'BR101', 'comp':2.5, 'ano':55} in incidentesDeRJ
    assert {'nome':'BR105', 'comp':2.1, 'ano':60} in incidentesDeRJ
    assert {'origem':'RJ', 'destino':'RJ'} in incidentesDeRJ
    assert {} in incidentesDeRJ
    assert {'origem':'RJ', 'destino':'RJ'} in incidentesEmRJ
    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesEmRJ

    grafo.desligar('RJ', 'PE', lambda lig: lig.get('comp', -1) == 2.5)

    incidentesEmPE = grafo.incidentesEm('PE')
    incidentesDePE = grafo.incidentesDe('PE')
    incidentesEmRJ = grafo.incidentesEm('RJ')
    incidentesDeRJ = grafo.incidentesDe('RJ')

    assert len(incidentesEmPE) is 3
    assert len(incidentesDePE) is 1
    assert len(incidentesDeRJ) is 5
    assert len(incidentesEmRJ) is 3

    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesDePE
    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesEmPE
    assert {'nome':'BR101', 'comp':2.5, 'ano':55} not in incidentesEmPE
    assert {'nome':'BR105', 'comp':2.1, 'ano':60} in incidentesEmPE
    assert {} in incidentesEmPE
    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesDeRJ
    assert {'nome':'BR101', 'comp':2.5, 'ano':55} not in incidentesDeRJ
    assert {'nome':'BR105', 'comp':2.1, 'ano':60} in incidentesDeRJ
    assert {'origem':'RJ', 'destino':'RJ'} in incidentesDeRJ
    assert {} in incidentesDeRJ
    assert {'origem':'RJ', 'destino':'RJ'} in incidentesEmRJ
    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesEmRJ

    grafo.desligar('RJ', 'RJ', lambda lig: lig.get('nome', -1) is 'retorno')

    incidentesEmPE = grafo.incidentesEm('PE')
    incidentesDePE = grafo.incidentesDe('PE')
    incidentesEmRJ = grafo.incidentesEm('RJ')
    incidentesDeRJ = grafo.incidentesDe('RJ')

    assert len(incidentesEmPE) is 3
    assert len(incidentesDePE) is 1
    assert len(incidentesDeRJ) is 4
    assert len(incidentesEmRJ) is 2

    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesDePE
    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesEmPE
    assert {'nome':'BR105', 'comp':2.1, 'ano':60} in incidentesEmPE
    assert {} in incidentesEmPE
    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesDeRJ
    assert {'nome':'BR105', 'comp':2.1, 'ano':60} in incidentesDeRJ
    assert {'nome':'retorno'} not in incidentesDeRJ
    assert {'origem':'RJ', 'destino':'RJ'} in incidentesDeRJ
    assert {} in incidentesDeRJ
    assert {'origem':'RJ', 'destino':'RJ'} in incidentesEmRJ
    assert {'nome':'BR101', 'comp':1.4, 'ano':53} in incidentesEmRJ
    assert {'nome': 'retorno'} not in incidentesEmRJ

    grafo.desligar('PE', 'RJ', lambda lig: lig.get('nome', -1) is 'BR101')

    incidentesEmPE = grafo.incidentesEm('PE')
    incidentesDePE = grafo.incidentesDe('PE')
    incidentesEmRJ = grafo.incidentesEm('RJ')
    incidentesDeRJ = grafo.incidentesDe('RJ')

    assert len(incidentesEmPE) is 2
    assert len(incidentesDePE) is 0
    assert len(incidentesDeRJ) is 3
    assert len(incidentesEmRJ) is 1

    assert {'nome':'BR101', 'comp':1.4, 'ano':53} not in incidentesDePE
    assert {'nome':'BR101', 'comp':1.4, 'ano':53} not in incidentesEmPE
    assert {'nome':'BR105', 'comp':2.1, 'ano':60} in incidentesEmPE
    assert {} in incidentesEmPE
    assert {'nome':'BR101', 'comp':1.4, 'ano':53} not in incidentesDeRJ
    assert {'nome':'BR105', 'comp':2.1, 'ano':60} in incidentesDeRJ
    assert {'origem':'RJ', 'destino':'RJ'} in incidentesDeRJ
    assert {} in incidentesDeRJ
    assert {'origem':'RJ', 'destino':'RJ'} in incidentesEmRJ
    assert {'nome':'BR101', 'comp':1.4, 'ano':53} not in incidentesEmRJ

    grafo.desligar('RJ', 'PE')

    assert grafo.incidentesEm('PE') == grafo.incidentesDe('PE') == tuple()

    assert grafo.incidentesDe('RJ') == grafo.incidentesEm('RJ') == \
           ({'origem':'RJ', 'destino':'RJ'}, )


def testes_desligar_lancaraQualquerErroGeradoPelaFiltragemDasLigacoes():
    with raises(KeyError):
        grafo.desligar('RJ', 'SP', lambda lig: lig['chave inexistente'])


def testes_desligar_geraUmErroSeUmDosItensNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        grafo.desligar('-', 'PE')

    with raises(ItemNaoEncontrado):
        grafo.desligar('PE', '-')


def testes_desligar_removeTodasAsLigacoesDeAParaBSeOFiltroNaoForInformado():
    grafo = novoGrafo('PE', 'RJ')
    grafo.ligar('PE', 'RJ')
    grafo.ligar('PE', 'RJ', NAO_ORIENTADA)
    grafo.ligar('PE', 'RJ', nome='BR101', comp=63, ano=56)
    grafo.ligar('PE', 'RJ', NAO_ORIENTADA, nome='BR105', km=77, idade=33)
    grafo.ligar('PE', 'RJ', id=44)
    grafo.ligar('PE', 'RJ', estado='em construção')
    grafo.ligar('PE', 'RJ', estado='finalizada', ano=2017)
    grafo.ligar('PE', 'RJ', NAO_ORIENTADA, categoria='rodoviaria')
    grafo.ligar('PE', 'RJ', categoria='aerea')
    grafo.ligar('PE', 'RJ', categoria='aquatica') # 10 ligações

    grafo.desligar('PE', 'RJ')

    assert vazio(grafo.incidentesDe('PE'))
    assert vazio(grafo.incidentesEm('PE'))
    assert vazio(grafo.incidentesDe('RJ'))
    assert vazio(grafo.incidentesEm('RJ'))


def testes_totalDeLigacoesOrientadas_e_NaoOrientadas_aposDesligarVertices():
    grafo = novoGrafo('AM', 'PE', 'RJ', 'SP')
    grafo.ligar('PE', 'RJ', NAO_ORIENTADA)
    grafo.ligar('RJ', 'PE', nome='BR101', km=1344)
    grafo.ligar('RJ', 'PE', nome='BR105', comp=1557)
    grafo.ligar('SP', 'PE', categoria='aerea')
    grafo.ligar('PE', 'AM', NAO_ORIENTADA, categoria='trem', ano=97, id='003')
    grafo.ligar('SP', 'AM', nome='BR102', ano=1987)
    grafo.ligar('PE', 'AM', NAO_ORIENTADA, id='001', km=1620)
    grafo.ligar('PE', 'AM', NAO_ORIENTADA, id='002', comp=1700, ano=1788)

    grafo.desligar('RJ', 'PE', lambda ligacao: ligacao == dict())

    assert grafo.totalDeLigacoesNaoOrientadas is 3
    assert grafo.totalDeLigacoesOrientadas is 4

    grafo.desligar('SP', 'AM')
    grafo.desligar('SP', 'PE')

    assert grafo.totalDeLigacoesNaoOrientadas is 3
    assert grafo.totalDeLigacoesOrientadas is 2

    grafo.desligar('RJ', 'PE', lambda ligacao: ligacao['nome'] is 'BR105')
    grafo.desligar('PE', 'AM', lambda ligacao: ligacao['id'] is '002')

    assert grafo.totalDeLigacoesNaoOrientadas is 2
    assert grafo.totalDeLigacoesOrientadas is 1

    grafo.desligar('PE', 'AM')
    grafo.desligar('RJ', 'PE')

    assert grafo.totalDeLigacoesNaoOrientadas is 0
    assert grafo.totalDeLigacoesOrientadas is 0


def testes_desligar_naoRemoveraALigacaoDeBParaAMesmoQueElaPasassePeloFiltro():
    grafo = novoGrafo('AM', 'PE')
    grafo.ligar('PE', 'AM', nome='BR10', ano=65)
    grafo.ligar('AM', 'PE', nome='BR10', ano=65)
    grafo.desligar('PE', 'AM')

    assert grafo.incidentesEm('PE') == grafo.incidentesDe('AM') == \
           ({'nome':'BR10', 'ano':65}, )
    assert vazio(grafo.incidentesDe('PE'))
    assert vazio(grafo.incidentesEm('AM'))


def testes_remover():
    grafo = grafoDeTestes()
    grafo.remover('AM')

    assert contemApenas((pe_mt_pe, pe_rn, pe_rj), grafo.incidentesDe('PE'))
    assert contemApenas((pe_mt_pe, sp_pe, pb_pe), grafo.incidentesEm('PE'))
    assert 'AM' not in grafo

    grafo.remover('RJ')

    assert 'RJ' not in grafo
    assert grafo.incidentesDe('SP') == (sp_pe, )
    assert vazio(grafo.incidentesEm('SP'))
    assert pe_rj not in grafo.incidentesDe('PE')

    grafo.remover('PB')

    assert 'PB' not in grafo
    assert contemApenas((mt_rn1, mt_rn2, mt_rn3, pe_rn), grafo.incidentesEm('RN'))
    assert grafo.incidentesDe('RN') == (rn_mt, )
    assert contemApenas((pe_mt_pe, sp_pe), grafo.incidentesEm('PE'))

    grafo.remover('MT')

    assert 'MT' not in grafo
    assert vazio(grafo.incidentesDe('RN'))
    assert grafo.incidentesEm('RN') == (pe_rn, )
    assert grafo.incidentesDe('PE') == (pe_rn, )
    assert grafo.incidentesEm('PE') == (sp_pe, )


def testes_totalDeLigacoesOrientadas_e_NaoOrientadas_aposRemoverVertices():
    grafo = grafoDeTestes()
    grafo.remover('AM')

    assert grafo.totalDeLigacoesNaoOrientadas is 3
    assert grafo.totalDeLigacoesOrientadas is 11

    grafo.remover('SP')

    assert grafo.totalDeLigacoesNaoOrientadas is 2
    assert grafo.totalDeLigacoesOrientadas is 10

    grafo.remover('MT')

    assert grafo.totalDeLigacoesNaoOrientadas is 1
    assert grafo.totalDeLigacoesOrientadas is 6

    grafo.remover('RN')

    assert grafo.totalDeLigacoesNaoOrientadas is 0
    assert grafo.totalDeLigacoesOrientadas is 2


def testes_totalDeItens_aposRemoverItens():
    grafo = grafoDeTestes()
    grafo.remover('PE')

    assert grafo.totalDeItens is 7

    grafo.remover('SP')
    grafo.remover('RJ')

    assert grafo.totalDeItens is 5

    grafo.remover('MT')
    grafo.remover('PB')
    grafo.remover('RN')

    assert grafo.totalDeItens is 2


def testes_remover_retornaNormalmenteSeOItemNaoForLocalizado():
    with naoGeraErro():
        grafo.remover('-')


def testes_ligacoes():
    ligacoes = grafo.ligacoes('MT', 'RN')
    assert len(ligacoes) is 3
    assert mt_rn1 in ligacoes
    assert mt_rn2 in ligacoes
    assert mt_rn3 in ligacoes

    assert grafo.ligacoes('RN', 'MT') == (rn_mt, )

    assert vazio(grafo.ligacoes('PB', 'AM'))

    assert grafo.ligacoes('AM', 'AM') == (am_am, )


def testes_ligacoes_retornaraUmaTuplaVaziaSe_a_naoForLocalizado():
    assert vazio(grafo.ligacoes('-', 'PE'))


def testes_ligacoes_retornaraUmaTuplaVaziaSe_b_naoForLocalizado():
    assert vazio(grafo.ligacoes('PE', '-'))


def testes_caminhosMinimos():
    grafo = novoGrafo('PE', 'SP', 'RJ', 'MT')
    grafo.ligar('PE', 'SP', distancia=800, id='015')
    grafo.ligar('SP', 'MT', distancia=800, id='020')
    grafo.ligar('SP', 'RJ', distancia=400, id='025')
    grafo.ligar('RJ', 'MT', distancia=400, id='030')

    caminhos = grafo.caminhosMinimos('PE', 'MT')

    assert len(caminhos) is 2

    assert {'origem':'PE', 'dest':'MT', 'total':3, 'distancia':1600,
            'vertices':('PE', 'SP', 'MT'),
            'trechos':{('PE', 'SP'):{'distancia':800, 'id':'015'},
                       ('SP', 'MT'):{'distancia':800, 'id':'020'}}} in caminhos

    assert {'origem':'PE', 'dest':'MT', 'total':4, 'distancia':1600,
            'vertices':('PE', 'SP', 'RJ', 'MT'),
            'trechos':{('PE', 'SP'):{'distancia':800, 'id':'015'},
                       ('SP', 'RJ'):{'distancia':400, 'id':'025'},
                       ('RJ', 'MT'):{'distancia':400, 'id':'030'}}} in caminhos

    grafo.ligar('SP', 'MT', id='035')
    grafo.ligar('RJ', 'MT', id='040')
    grafo.ligar('PE', 'MT', id='045')

    caminhos = grafo.caminhosMinimos('PE', 'MT')

    assert len(caminhos) is 2

    assert {'origem':'PE', 'dest':'MT', 'total':3, 'distancia':1600,
            'vertices':('PE', 'SP', 'MT'),
            'trechos':{('PE', 'SP'):{'distancia':800, 'id':'015'},
                       ('SP', 'MT'):{'distancia':800, 'id':'020'}}} in caminhos

    assert {'origem':'PE', 'dest':'MT', 'total':4, 'distancia':1600,
            'vertices':('PE', 'SP', 'RJ', 'MT'),
            'trechos':{('PE', 'SP'):{'distancia':800, 'id':'015'},
                       ('SP', 'RJ'):{'distancia':400, 'id':'025'},
                       ('RJ', 'MT'):{'distancia':400, 'id':'030'}}} in caminhos

    grafo.ligar('PE', 'MT', distancia=1300, id='050')

    assert grafo.caminhosMinimos('PE', 'MT') == \
           [{'origem':'PE', 'dest':'MT', 'total':2, 'distancia':1300,
            'vertices':('PE', 'MT'), 'id':'050'}]


def testes_caminhosMinimos_retornaraUmaListaVaziaSeNaoHouverCaminhoDeAparaB():
    assert vazio(grafo.caminhosMinimos('AM', 'SP'))


def testes_caminhosMinimos_retornaraUmaListaVaziaSeAsDistanciasDeTodosOsCaminhosDeAparaBForemIndefinidas():
    grafo = novoGrafo('PE', 'SP', 'RJ', 'MT')
    grafo.ligar('PE', 'SP', distancia=800, id='010')
    grafo.ligar('SP', 'MT', id='015')
    grafo.ligar('SP', 'RJ', id='020')
    grafo.ligar('RJ', 'MT', distancia=400, id='025')
    grafo.ligar('PE', 'MT', id='030')

    assert vazio(grafo.caminhosMinimos('PE', 'MT'))


def testes_caminhosMinimos_iraGerarUmErroSeANaoForLocalizado():
    with raises(ItemNaoEncontrado):
        grafo.caminhosMinimos('QW', 'PE')


def testes_caminhosMinimos_iraGerarUmErroSeBNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        grafo.caminhosMinimos('PE', 'QW')


def testes_arvoreCoberturaMinima_caso1():
    # funciona apenas com grafos ñ dirigidos e conexos
    grafo = novoGrafo('AM', 'PE', 'SP', 'RJ', 'MT', 'RN', 'PB')

    grafo.ligar('PE', 'AM', NAO_ORIENTADA, **pe_am)
    grafo.ligar('SP', 'PE', NAO_ORIENTADA, **sp_pe)
    grafo.ligar('RN', 'MT', NAO_ORIENTADA, **rn_mt)
    grafo.ligar('PB', 'RN', NAO_ORIENTADA, **pb_rn1)
    grafo.ligar('AM', 'AM', NAO_ORIENTADA, **am_am)
    grafo.ligar('PE', 'RJ', NAO_ORIENTADA, **pe_rj)
    grafo.ligar('MT', 'RN', NAO_ORIENTADA, **mt_rn1)
    grafo.ligar('MT', 'RN', NAO_ORIENTADA, **mt_rn2)
    grafo.ligar('MT', 'RN', NAO_ORIENTADA, **mt_rn3)
    grafo.ligar('RN', 'PB', NAO_ORIENTADA, **rn_pb)
    grafo.ligar('PB', 'RN', NAO_ORIENTADA, **pb_rn2)
    grafo.ligar('PE', 'RN', NAO_ORIENTADA, **pe_rn)
    grafo.ligar('PB', 'PE', NAO_ORIENTADA, **pb_pe)
    grafo.ligar('SP', 'RJ', NAO_ORIENTADA, **sp_rj_sp)
    grafo.ligar('RN', 'PB', NAO_ORIENTADA, **rn_pb_rn)
    grafo.ligar('PE', 'MT', NAO_ORIENTADA, **pe_mt_pe)

    grafo = grafo.arvoreCoberturaMinima()

    assert contemApenas((pe_am, pe_rj, pe_mt_pe, pb_pe), grafo.incidentesEm('PE'))
    assert contemApenas((pe_am, pe_rj, pe_mt_pe, pb_pe), grafo.incidentesDe('PE'))
    assert grafo.incidentesEm('AM') == (pe_am, )
    assert grafo.incidentesDe('AM') == (pe_am, )
    assert grafo.incidentesEm('SP') == (sp_rj_sp, )
    assert grafo.incidentesDe('SP') == (sp_rj_sp, )
    assert contemApenas((sp_rj_sp, pe_rj), grafo.incidentesEm('RJ'))
    assert contemApenas((sp_rj_sp, pe_rj), grafo.incidentesDe('RJ'))
    assert grafo.incidentesEm('MT') == (pe_mt_pe, )
    assert grafo.incidentesDe('MT') == (pe_mt_pe, )
    assert grafo.incidentesEm('RN') == (rn_pb_rn, )
    assert grafo.incidentesDe('RN') == (rn_pb_rn, )
    assert contemApenas((rn_pb_rn, pb_pe), grafo.incidentesEm('PB'))
    assert contemApenas((rn_pb_rn, pb_pe), grafo.incidentesDe('PB'))


def testes_arvoreCoberturaMinima_caso2():
    grafo = novoGrafo('BOS', 'PVD', 'ORD', 'JFK', 'BWI', 'SFO', 'DFW',
                      'LAX', 'MIA')
    grafo.ligar('BOS', 'SFO', NAO_ORIENTADA, distancia=2704, id='01')
    grafo.ligar('BOS', 'MIA', NAO_ORIENTADA, distancia=1258, id='02')
    grafo.ligar('BOS', 'ORD', NAO_ORIENTADA, distancia=867, id='03')
    grafo.ligar('BOS', 'JFK', NAO_ORIENTADA, distancia=187, id='04')
    grafo.ligar('ORD', 'PVD', NAO_ORIENTADA, distancia=849, id='05')
    grafo.ligar('PVD', 'JFK', NAO_ORIENTADA, distancia=144, id='06')
    grafo.ligar('ORD', 'JFK', NAO_ORIENTADA, distancia=740, id='07')
    grafo.ligar('ORD', 'BWI', NAO_ORIENTADA, distancia=621, id='08')
    grafo.ligar('ORD', 'SFO', NAO_ORIENTADA, distancia=1846, id='09')
    grafo.ligar('ORD', 'DFW', NAO_ORIENTADA, distancia=802, id='10')
    grafo.ligar('JFK', 'DFW', NAO_ORIENTADA, distancia=1391, id='11')
    grafo.ligar('JFK', 'BWI', NAO_ORIENTADA, distancia=184, id='12')
    grafo.ligar('JFK', 'MIA', NAO_ORIENTADA, distancia=1090, id='13')
    grafo.ligar('SFO', 'DFW', NAO_ORIENTADA, distancia=1464, id='14')
    grafo.ligar('LAX', 'DFW', NAO_ORIENTADA, distancia=1235, id='15')
    grafo.ligar('SFO', 'LAX', NAO_ORIENTADA, distancia=337, id='16')
    grafo.ligar('DFW', 'MIA', NAO_ORIENTADA, distancia=1121, id='17')
    grafo.ligar('BWI', 'MIA', NAO_ORIENTADA, distancia=946, id='18')
    grafo.ligar('LAX', 'MIA', NAO_ORIENTADA, distancia=2342, id='19')

    grafo = grafo.arvoreCoberturaMinima()

    assert grafo.incidentesDe('BOS') == ({'distancia':187, 'id':'04'}, )
    assert grafo.incidentesEm('BOS') == ({'distancia':187, 'id':'04'}, )
    assert grafo.incidentesDe('PVD') == ({'distancia':144, 'id':'06'}, )
    assert grafo.incidentesEm('PVD') == ({'distancia':144, 'id':'06'}, )
    assert contemApenas(({'distancia':802, 'id':'10'},
                         {'distancia':621, 'id':'08'}), grafo.incidentesDe('ORD'))
    assert contemApenas(({'distancia':802, 'id':'10'},
                         {'distancia':621, 'id':'08'}), grafo.incidentesEm('ORD'))

    assert contemApenas(({'distancia':187, 'id':'04'},
                         {'distancia':144, 'id':'06'},
                         {'distancia':184, 'id':'12'}), grafo.incidentesDe('JFK'))
    assert contemApenas(({'distancia':187, 'id':'04'},
                         {'distancia':144, 'id':'06'},
                         {'distancia':184, 'id':'12'}), grafo.incidentesEm('JFK'))

    assert contemApenas(({'distancia':621, 'id':'08'},
                         {'distancia':184, 'id':'12'},
                         {'distancia':946, 'id':'18'}), grafo.incidentesEm('BWI'))
    assert contemApenas(({'distancia':621, 'id':'08'},
                         {'distancia':184, 'id':'12'},
                         {'distancia':946, 'id':'18'}), grafo.incidentesDe('BWI'))

    assert contemApenas(({'distancia':802, 'id':'10'},
                         {'distancia':1235, 'id':'15'}), grafo.incidentesDe('DFW'))
    assert contemApenas(({'distancia':802, 'id':'10'},
                         {'distancia':1235, 'id':'15'}), grafo.incidentesEm('DFW'))

    assert contemApenas(({'distancia':337, 'id':'16'},
                         {'distancia':1235, 'id':'15'}), grafo.incidentesDe('LAX'))
    assert contemApenas(({'distancia':337, 'id':'16'},
                         {'distancia':1235, 'id':'15'}), grafo.incidentesEm('LAX'))

    assert grafo.incidentesDe('SFO') == ({'distancia':337, 'id':'16'}, )
    assert grafo.incidentesEm('SFO') == ({'distancia':337, 'id':'16'}, )
    assert grafo.incidentesDe('MIA') == ({'distancia':946, 'id':'18'}, )
    assert grafo.incidentesEm('MIA') == ({'distancia':946, 'id':'18'}, )


def testes_arvoreCoberturaMinima_caso3():
    """arvoreCoberturaMinima retornará normalmente mesmo se o grafo possuir
    ligações sem a distância informada mas for possível determinar a acm"""
    grafo = novoGrafo('AM', 'PE', 'RJ')
    grafo.ligar('AM', 'PE', NAO_ORIENTADA, distancia=1000, id='1')
    grafo.ligar('AM', 'PE', NAO_ORIENTADA, id='2')
    grafo.ligar('PE', 'RJ', NAO_ORIENTADA, distancia=1300, id='3')
    grafo.ligar('PE', 'RJ', NAO_ORIENTADA, id='4')

    grafo = grafo.arvoreCoberturaMinima()

    assert grafo.incidentesDe('AM') == ({'distancia':1000, 'id':'1'}, )
    assert grafo.incidentesEm('AM') == ({'distancia':1000, 'id':'1'}, )
    assert contemApenas(({'distancia':1000, 'id':'1'},
                         {'distancia':1300, 'id':'3'}),
                        grafo.incidentesDe('PE'))
    assert contemApenas(({'distancia':1000, 'id':'1'},
                         {'distancia':1300, 'id':'3'}),
                        grafo.incidentesEm('PE'))
    assert grafo.incidentesDe('RJ') == ({'distancia':1300, 'id':'3'}, )
    assert grafo.incidentesEm('RJ') == ({'distancia':1300, 'id':'3'}, )


def testes_arvoreCoberturaMinima_iraGerarUmErroSeOGrafoPossuirLigacoesOrientadas():
    grafo = novoGrafo('PE', 'AM')
    grafo.ligar('PE', 'AM', distancia=1000)
    grafo.ligar('AM', 'PE', NAO_ORIENTADA, distancia=1000)

    with raises(FalhaNaOperacao):
        grafo.arvoreCoberturaMinima()


def testes_arvoreCoberturaMinima_retornaraUmGrafoVazioSeOOriginalEstiverVazio():
    grafo = Grafo().arvoreCoberturaMinima()

    assert grafo.totalDeLigacoes is 0
    assert grafo.totalDeItens is 0


def testes1_arvoreCoberturaMinima_iraGerarUmErroSeNaoForPossivelDeterminarAACM():
    grafo = novoGrafo('PE', 'AM')
    grafo.ligar('PE', 'AM', NAO_ORIENTADA)

    with raises(FalhaNaOperacao):
        grafo.arvoreCoberturaMinima()


def testes2_arvoreCoberturaMinima_iraGerarUmErroSeNaoForPossivelDeterminarAACM():
    grafo = novoGrafo('PE', 'AM', 'RJ')

    grafo.ligar('PE', 'AM', NAO_ORIENTADA)
    grafo.ligar('PE', 'RJ', NAO_ORIENTADA, distancia=1300)

    with raises(FalhaNaOperacao):
        grafo.arvoreCoberturaMinima()


def testes_arvoreCoberturaMinima_iraGerarUmErroSeOGrafoNaoForConexo():
    grafo = novoGrafo('KW', 'PE', 'AM')
    grafo.ligar('AM', 'PE', NAO_ORIENTADA, distancia=1000)

    with raises(Exception):
        grafo.arvoreCoberturaMinima()




