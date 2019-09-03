from grafo import Grafo
from pytest import raises
from erros import ItemNaoEncontrado
from iteruteis import vazio


grafo = Grafo().ligacoes_simples()
ngrafo = Grafo().ligacoes_com_informacoes2()

# não há ligações múltiplas no grafo

def testes_metodo_caminhos():
    assert ngrafo.caminhos('PE', 'AM') == (('PE', 'AM'), )

    caminhos = ngrafo.caminhos('SP', 'RJ')

    assert len(caminhos) is 2
    assert ('SP', 'RJ') in caminhos
    assert ('SP', 'PE', 'RJ') in caminhos

    caminhos = ngrafo.caminhos('RN', 'PE')

    assert len(caminhos) is 3
    assert ('RN', 'PE') in caminhos
    assert ('RN', 'MT', 'PE') in caminhos
    assert ('RN', 'PB', 'PE') in caminhos


def testes_oMetodo_caminhos_retornaUmaTuplaVaziaSeNaoHouverCaminhoDeAParaB():
    assert vazio(grafo.caminhos('AM', 'XY'))


def testes_oMetodo_caminhos_iraGerarUmErroSeANaoForLocalizado():
    with raises(ItemNaoEncontrado):
        grafo.caminhos('QW', 'PE')


def testes_oMetodo_caminhos_iraGerarUmErroSeBNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        grafo.caminhos('PE', 'QW')


def testes_metodo_caminhos_retornaraTodosOsLacosSeAeBForemOsMesmos():
    caminhos = ngrafo.caminhos('SP', 'SP')

    assert  len(caminhos) is 4
    assert ('SP', 'RJ', 'SP') in caminhos
    assert ('SP', 'PE', 'SP') in caminhos
    assert ('SP', 'PE', 'RJ', 'SP') in caminhos
    assert ('SP', 'RJ', 'PE', 'SP') in caminhos

    caminhos = ngrafo.caminhos('AM', 'AM')
    assert ('AM', 'AM') in caminhos


def testes_metodo_trajetos():
    trajetos = ngrafo.trajetos('PE', 'AM')

    assert len(trajetos) is 1
    assert {'origem':'PE', 'dest':'AM', 'distancia':2833, 'id':'010',
    'total':2, 'vertices':('PE', 'AM')} in trajetos

    trajetos = ngrafo.trajetos('SP', 'RJ')

    assert len(trajetos) is 2

    assert {'origem':'SP', 'dest':'RJ', 'distancia':357, 'id':'030',
    'total':2, 'vertices':('SP', 'RJ')} in trajetos

    assert {'origem':'SP', 'dest':'RJ', 'total':3,
            'vertices':('SP', 'PE', 'RJ'),
            'trechos':{('SP', 'PE'): {'distancia':2128, 'id':'025'},
                       ('PE', 'RJ'): {'distancia':1874, 'id':'020'}}
            } in trajetos


    trajetos = ngrafo.trajetos('PB', 'SP')

    assert len(trajetos) is 6
    assert {'origem':'PB', 'dest':'SP', 'total':3,
            'vertices':('PB', 'PE', 'SP'),
            'trechos':{('PB', 'PE'): {'distancia':104, 'id':'055'},
                       ('PE', 'SP'): {'distancia':2128, 'id':'025'}}
            } in trajetos

    assert {'origem':'PB', 'dest':'SP', 'total':4,
            'vertices':('PB', 'PE', 'RJ', 'SP'),
            'trechos':{('PB', 'PE'):{'distancia':104, 'id':'055'},
                       ('PE', 'RJ'):{'distancia':1874, 'id':'020'},
                       ('RJ', 'SP'):{'distancia':357, 'id':'030'}}
            } in trajetos

    assert {'origem':'PB', 'dest':'SP', 'total':4,
            'vertices':('PB', 'RN', 'PE', 'SP'),
            'trechos':{('PB', 'RN'):{'distancia':151, 'id':'040'},
                       ('RN', 'PE'):{'distancia':253, 'id':'050'},
                       ('PE', 'SP'):{'distancia':2128, 'id':'025'}}} \
           in trajetos

    assert {'origem':'PB', 'dest':'SP', 'total':5,
            'vertices':('PB', 'RN', 'PE', 'RJ', 'SP'),
            'trechos':{('PB', 'RN'):{'distancia':151, 'id':'040'},
                       ('RN', 'PE'):{'distancia':253, 'id':'050'},
                       ('PE', 'RJ'):{'distancia':1874, 'id':'020'},
                       ('RJ', 'SP'):{'distancia':357, 'id':'030'}}} \
           in trajetos

    assert {'origem': 'PB', 'dest': 'SP', 'total': 5,
            'vertices':('PB', 'RN', 'MT', 'PE', 'SP'),
            'trechos':{('PB', 'RN'):{'distancia':151, 'id':'040'},
                       ('RN', 'MT'):{'distancia':2524, 'id':'035'},
                       ('MT', 'PE'):{'distancia':2452, 'id':'045'},
                       ('PE', 'SP'):{'distancia':2128, 'id':'025'}}} \
           in trajetos

    assert {'origem': 'PB', 'dest': 'SP', 'total': 6,
            'vertices':('PB', 'RN', 'MT', 'PE', 'RJ', 'SP'),
            'trechos':{('PB', 'RN'):{'distancia':151, 'id':'040'},
                       ('RN', 'MT'):{'distancia':2524, 'id':'035'},
                       ('MT', 'PE'):{'distancia':2452, 'id':'045'},
                       ('PE', 'RJ'): {'distancia': 1874, 'id': '020'},
                       ('RJ', 'SP'): {'distancia': 357, 'id': '030'}}} \
           in trajetos


def testes_metodo_trajetos_comA_igualA_B():
    # am está ligado a ele mesmo, há um laço self, está se testando o
    # código com um laço self
    trajetos = ngrafo.trajetos('AM', 'AM')

    assert len(trajetos) is 2
    assert {'origem':'AM', 'dest':'AM', 'total':3,
            'vertices':('AM', 'PE', 'AM'),
            'trechos':{('AM', 'PE'):{'distancia':2833, 'id':'010'},
                       ('PE', 'AM'): {'distancia': 2833, 'id': '010'},
                       }} in trajetos

    assert {'origem':'AM', 'dest':'AM', 'vertices':('AM', 'AM'), 'total':2,
            'km':300, 'nome':'Estrada de Retorno'} in trajetos

    trajetos = ngrafo.trajetos('RJ', 'RJ')

    assert len(trajetos) is 4
    assert {'origem':'RJ', 'dest':'RJ', 'total':3,
            'vertices':('RJ', 'SP', 'RJ'),
            'trechos':{('RJ', 'SP'):{'distancia':357, 'id':'030'},
                       ('SP', 'RJ'):{'distancia':357, 'id':'030'}}} in trajetos

    assert {'origem':'RJ', 'dest':'RJ', 'total':3,
            'vertices':('RJ', 'PE', 'RJ'),
            'trechos':{('RJ', 'PE'):{'distancia':1874, 'id':'020'},
                       ('PE', 'RJ'):{'distancia':1874, 'id':'020'}}} in trajetos

    assert {'origem':'RJ', 'dest':'RJ', 'total':4,
            'vertices':('RJ', 'PE', 'SP', 'RJ'),
            'trechos':{('RJ', 'PE'):{'distancia':1874, 'id':'020'},
                       ('PE', 'SP'):{'distancia':2128, 'id':'025'},
                       ('SP', 'RJ'):{'distancia':357, 'id':'030'}}} in trajetos

    assert {'origem':'RJ', 'dest':'RJ', 'total':4,
            'vertices':('RJ', 'SP', 'PE', 'RJ'),
            'trechos':{('RJ', 'SP'):{'distancia':357, 'id':'030'},
                       ('SP', 'PE'):{'distancia':2128, 'id':'025'},
                       ('PE', 'RJ'):{'distancia':1874, 'id':'020'}}} in trajetos


def testes_oMetodo_trajetos_iraGerarUmErroSeANaoForLocalizado():
    with raises(ItemNaoEncontrado):
        ngrafo.trajetos('QW', 'PE')


def testes_oMetodo_trajetos_iraGerarUmErroSeBNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        ngrafo.trajetos('PE', 'QW')


def testes_oMetodo_trajetos_retornaUmaListaVaziaSeNaoHouverCaminhoDeAParaB():
    assert vazio(ngrafo.trajetos('PB', 'XY'))


