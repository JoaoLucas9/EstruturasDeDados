from skipList import SkipList
from arvore import IGUAIS
from erros import ItemNaoEncontrado, ColecaoVazia
from pytest import raises


def listaVazia():
    return SkipList(lambda c1, c2: IGUAIS if c1 == c2 else max(c1, c2))


def listaDeTestes():
    precos = SkipList(lambda c1, c2: IGUAIS if c1 == c2 else max(c1, c2))
    precos[2] = 'caneta'
    precos[100] = 'uniforme'
    precos[60] = 'fone'
    precos[15] = 'estojo'
    precos[30] = 'livro'
    precos[5] = 'regua'
    precos[50] = 'mochila'
    precos[10] = 'caderno'

    return precos


lista = listaDeTestes()



def testes_metodo_setitem():
    precos = SkipList(lambda c1, c2: IGUAIS if c1 == c2 else max(c1, c2))
    precos[2] = 'caneta'
    precos[5] = 'regua'
    precos[10] = 'caderno'
    precos[15] = 'estojo'
    precos[30] = 'livro'
    precos[100] = 'uniforme'

    assert precos[2] == 'caneta'
    assert precos[5] == 'regua'
    assert precos[10] == 'caderno'
    assert precos[15] == 'estojo'
    assert precos[30] == 'livro'
    assert precos[100] == 'uniforme'


def testes_metodo_setitem_alterarOValorAssociadoAUmaChave():
    precos = SkipList(lambda c1, c2: IGUAIS if c1 == c2 else max(c1, c2))
    precos[2] = 'caneta'
    precos[5] = 'regua'
    precos[10] = 'caderno'

    precos[5] = 'apontador'
    precos[10] = 'marcador'

    assert precos[5] == 'apontador'
    assert precos[10] == 'marcador'


def testes_metodo_setitem_informarUmCallable():
    precos = SkipList(lambda c1, c2: IGUAIS if c1 == c2 else max(c1, c2))
    precos['caneta'] = 2

    precos['caneta'] = lambda c, v: v * 2
    precos['caderno'] = lambda c, v: 20

    assert precos['caneta'] == 4
    assert precos['caderno'] == 20


def testes_propiedade_tamanho_aposInserirAlgunsPares():
    precos = SkipList(lambda c1, c2: IGUAIS if c1 == c2 else max(c1, c2))
    precos[2] = 'caneta'
    precos[5] = 'regua'
    precos[10] = 'caderno'

    assert precos.tamanho == 3

    precos[15] = 'estojo'
    precos[30] = 'livro'

    assert precos.tamanho == 5

    precos[50] = 'mochila'

    assert precos.tamanho == 6


# os place holders devem ser invisíveis, os clientes não devem saber da sua
# existência
def testes_metodo_parMenorIgual():
    par = lista.parMenorIgual(2)
    assert par.chave == 2
    assert par.valor == 'caneta'

    par = lista.parMenorIgual(7)
    assert par.chave == 5
    assert par.valor == 'regua'

    par = lista.parMenorIgual(100)
    assert par.chave == 100
    assert par.valor == 'uniforme'

    par = lista.parMenorIgual(1_000)
    assert par.chave == 100
    assert par.valor == 'uniforme'


def testes_oMetodo_maiorChave_geraUmErroSeNaoHouverUmaChaveMenorIgualAInformada():
    with raises(ItemNaoEncontrado):
        lista.parMenorIgual(1)

    with raises(ItemNaoEncontrado):
        lista.parMenorIgual(-1_000)


def testes_metodo_parMaiorIgual():
    par = lista.parMaiorIgual(2)
    assert par.chave == 2
    assert par.valor == 'caneta'

    par = lista.parMaiorIgual(90)
    assert par.chave == 100
    assert par.valor == 'uniforme'

    par = lista.parMaiorIgual(-100)
    assert par.chave == 2
    assert par.valor == 'caneta'

    par = lista.parMaiorIgual(100)
    assert par.chave == 100
    assert par.valor == 'uniforme'


def testes_oMetodo_menorChave_geraUmErroSeNaoHouverUmaChaveMaiorIgualAInformada():
    with raises(ItemNaoEncontrado):
        lista.parMaiorIgual(150)


def testes_metodo_getitem():
    assert lista[2] is 'caneta'
    assert lista[100] is 'uniforme'
    assert lista[30] is 'livro'


def testes_oMetodo_getitem_geraUmErroSeAChaveNaoForLocalizada():
    with raises(ItemNaoEncontrado):
        lista[35]


def testes_operador_in():
    assert 50 in lista
    assert 2 in lista
    assert 100 in lista

    assert 27 not in lista
    assert -1 not in lista


def testes_operador_del():
    precos = listaDeTestes()

    del precos[50]
    del precos[2]

    assert 50 not in precos
    assert 2 not in precos
    assert 30 in precos
    assert 5 in precos

    del precos[30]
    del precos[5]

    assert 30 not in precos
    assert 5 not in precos
    assert 15 in precos
    assert 100 in precos

    del precos[15]
    del precos[100]

    assert 15 not in precos
    assert 100 not in precos
    assert 60 in precos
    assert 10 in precos

    del precos[60]
    del precos[10]

    assert 60 not in precos
    assert 10 not in precos


def testes_propiedade_tamanho_aposRemoverAlgunsPares():
    precos = listaDeTestes()
    del precos[30]

    assert precos.tamanho == 7

    del precos[100]
    del precos[5]

    assert precos.tamanho == 5

    del precos[60]
    del precos[15]
    del precos[10]

    assert precos.tamanho == 2

    del precos[2]
    del precos[50]

    assert precos.tamanho == 0


def testes_oOperador_del_geraUmErroSeAChaveNaoForLocalizada():
    with raises(ItemNaoEncontrado):
        lista[0]


def teste_doIterador():
    assert list(lista) == [2, 5, 10, 15, 30, 50, 60, 100]
    assert list(listaVazia()) == []


def teste_metodo_pares():
    p = [(2, 'caneta'), (5, 'regua'), (10, 'caderno'), (15, 'estojo'),
         (30, 'livro'), (50, 'mochila'), (60, 'fone'), (100, 'uniforme')]

    assert list((p.chave, p.valor) for p in lista.pares()) == p
    assert list(listaVazia().pares()) == []


def teste_metodo_valores():
    v = ['caneta', 'regua', 'caderno', 'estojo', 'livro', 'mochila', 'fone',
         'uniforme']

    assert list(lista.valores()) == v
    assert list(listaVazia().valores()) == []


def teste_metodo_menorChave():
    assert lista.menorChave() == 2


def teste_metodo_menorChave_geraUmErroSeAListaEstiverVazia():
    with raises(ColecaoVazia):
        listaVazia().menorChave()


def teste_metodo_maiorChave():
    assert lista.maiorChave() == 100


def teste_metodo_maiorChave_geraUmErroSeAListaEstiverVazia():
    with raises(ColecaoVazia):
        listaVazia().maiorChave()


def testes_propiedade_vazia():
    precos = listaVazia()

    assert precos.vazia

    precos['caneta'] = 2

    assert not precos.vazia

    del precos['caneta']

    assert precos.vazia


def teste_metodo_menorPar():
    par = lista.menorPar()

    assert par.chave == 2
    assert par.valor is 'caneta'


def teste_metodo_menorPar_geraUmErroSeAListaEstiverVazia():
    with raises(ColecaoVazia):
        listaVazia().menorPar()


def teste_metodo_maiorPar():
    par = lista.maiorPar()

    assert par.chave == 100
    assert par.valor is 'uniforme'


def teste_metodo_maiorPar_geraUmErroSeAListaEstiverVazia():
    with raises(ColecaoVazia):
        listaVazia().maiorPar()

