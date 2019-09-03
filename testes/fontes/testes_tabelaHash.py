from erros import ItemNaoEncontrado
from tabelaHash import TabelaHash
from pytest import raises


def codigoHash(chave: str):
    """Gera o código usando apenas os 10 primeiros caracteres da str,
    ou toda, se ela possuir menos que 10 caracteres."""
    return sum(ord(chave[i]) * (33 ** i) for i in range(min(len(chave), 10)))


def dataDaFundacaoDeGrandesEmpresas():
    t = TabelaHash(codigoHash)
    t['microsoft'] = 1975
    t['google'] = 1998
    t['apple'] = 1976
    t['facebook'] = 2004
    t['ibm'] = 1911

    return t


fundacao = dataDaFundacaoDeGrandesEmpresas()

def testes_oMetodo_setitem_informarUma():
    chaveQueNaoEstaNaTabelaEUmValor()
    chaveQueEstaNaTabelaEUmValor()

    chaveQueNaoEstaNaTabelaEUmaFuncao()
    chaveQueEstaNaTabelaEUmaFuncao()


def chaveQueNaoEstaNaTabelaEUmValor():
    """Um novo par chave-valor deverá ser inserido na tabela."""
    localizacao = TabelaHash(codigoHash)
    localizacao['brasil'] = 'america'
    localizacao['frança'] = 'europa'
    localizacao['australia'] = 'oceania'
    localizacao['china'] = 'asia'

    assert 'brasil' in localizacao
    assert 'frança' in localizacao
    assert 'australia' in localizacao
    assert 'china' in localizacao

    assert localizacao['brasil'] is 'america'
    assert localizacao['frança'] is 'europa'
    assert localizacao['australia'] is 'oceania'
    assert localizacao['china'] is 'asia'


def chaveQueEstaNaTabelaEUmValor():
    """O atual valor da chave deverá ser substituido."""
    fund = dataDaFundacaoDeGrandesEmpresas()
    fund['microsoft'] = 1990
    fund['google'] = 2000
    fund['ibm'] = 2010

    assert fund['microsoft'] == 1990
    assert fund['google'] == 2000
    assert fund['ibm'] == 2010


def chaveQueNaoEstaNaTabelaEUmaFuncao():
    """Serão informados a chave e None a função e o valor retornado será
    inserido na tabela juntamente com a chave"""
    t = TabelaHash(codigoHash)
    t['pão'] = lambda c, v: len(c)
    t['gato'] = lambda c, v: len(c)
    t['gatos'] = lambda c, v: len(c)

    assert t['pão'] == 3
    assert t['gato'] == 4
    assert t['gatos'] == 5


def chaveQueEstaNaTabelaEUmaFuncao():
    """Serão informados a função a chave e o valor atual da mesma, o qual
    será substituido pelo valor retornado pela função."""
    fund = dataDaFundacaoDeGrandesEmpresas()
    fund['apple'] = lambda c, v: v + 5
    fund['facebook'] = lambda c, v: v + 5
    fund['ibm'] = lambda c, v: v + 5

    assert fund['apple'] == 1981
    assert fund['facebook'] == 2009
    assert fund['ibm'] == 1916


def testes_operador_in():
    assert 'microsoft' in fundacao
    assert 'google' in fundacao
    assert 'ibm' in fundacao

    assert 'fox' not in fundacao
    assert 'cnn' not in fundacao
    assert 'cbn' not in fundacao


def testes_metodo_getitem():
    assert fundacao['apple'] == 1976
    assert fundacao['facebook'] == 2004
    assert fundacao['google'] == 1998


def testes_oMetodo_getitem_iraGerarUmErroSeAChaveNaoForLocalizada():
    with raises(ItemNaoEncontrado):
        fundacao['fox']


def testes_propiedade_tamanho_aposInserirAlgunsItens():
    localizacao = TabelaHash(codigoHash)

    assert localizacao.tamanho == 0

    localizacao['brasil'] = 'america'
    localizacao['frança'] = 'europa'

    assert localizacao.tamanho == 2

    localizacao['australia'] = 'oceania'
    localizacao['china'] = 'asia'

    assert localizacao.tamanho == 4

    localizacao['africa do sul'] = 'africa'
    localizacao['Villa las Estrellas'] = 'antardida'

    assert localizacao.tamanho == 6


def testes_rehash():
    """Após o rehash deseja-se saber se o estado da tabela está correto.
    Testes realizados:
    1) a tabela antiga foi substituida por uma nova e maior
    2) o fator de carga é menor que o limite estabelecido
    3) todas as entradas permanecem intactas
    4) o tamanho da nova tabela está correto
    5) a propiedade tamanho da tabela está de acordo com o esperado"""
    fund = TabelaHash(codigoHash, capacidade=2, fatorDeCargaMaximo=0.2)
    tabela = fund._tabela

    fund['microsoft'] = 1975

    assert fund._tabela is not tabela
    assert fund.fatorDeCarga < fund.limiteFatorDeCarga
    assert fund['microsoft'] == 1975
    assert len(fund._tabela) == 7
    assert fund.tamanho == 1

    tabela = fund._tabela
    fund['apple'] = 1976

    assert fund._tabela is not tabela
    assert fund.fatorDeCarga < fund.limiteFatorDeCarga
    assert fund['microsoft'] == 1975
    assert fund['apple'] == 1976
    assert len(fund._tabela) == 17
    assert fund.tamanho == 2

    tabela = fund._tabela
    fund['ibm'] = 1911
    fund['google'] = 1998

    assert fund._tabela is not tabela
    assert fund.fatorDeCarga < fund.limiteFatorDeCarga
    assert fund['microsoft'] == 1975
    assert fund['apple'] == 1976
    assert fund['ibm'] == 1911
    assert fund['google'] == 1998
    assert len(fund._tabela) == 37
    assert fund.tamanho == 4


def testes_rehash_decrementar_limiteFatorDeCarga():
    fund = TabelaHash(codigoHash, capacidade=17)

    tabela = fund._tabela
    fund['microsoft'] = 1975
    fund['google'] = 1998
    fund['apple'] = 1976
    fund['facebook'] = 2004

    assert fund._tabela is tabela

    fund.limiteFatorDeCarga = 0.2

    assert fund._tabela is not tabela
    assert fund.fatorDeCarga < fund.limiteFatorDeCarga
    assert len(fund._tabela) == 37


def testes_reconfigurarPropiedade_limiteFatorDeCarga():
    t = TabelaHash(codigoHash)
    t.limiteFatorDeCarga = 0.2

    assert t.limiteFatorDeCarga == 0.2

    t.limiteFatorDeCarga = 0.7

    assert t.limiteFatorDeCarga == 0.7

    t.limiteFatorDeCarga = 0.9

    assert t.limiteFatorDeCarga == 0.9


def testes_propiedade_rehashsExecutados():
    fund = TabelaHash(codigoHash, capacidade=2, fatorDeCargaMaximo=0.2)

    fund['microsoft'] = 1975
    assert fund.rehashsExecutados == 1

    fund['apple'] = 1976
    assert fund.rehashsExecutados == 2

    fund['ibm'] = 1911
    fund['google'] = 1998
    assert fund.rehashsExecutados == 3

    fund['amazon'] = 1994
    fund['ebay'] = 1995
    fund['sony'] = 1946
    fund['nokia'] = 1865
    assert fund.rehashsExecutados == 4


def testes_propiedade_totalDeColisoes():
    fund = TabelaHash(lambda texto: len(texto), capacidade=2, fatorDeCargaMaximo=0.2)

    fund['apple'] = 1976
    fund['nokia'] = 1865
    assert fund.totalDeColisoes == 1

    fund['ebay'] = 1995
    fund['sony'] = 1946
    assert fund.totalDeColisoes == 2

    fund['google'] = 1998
    fund['amazon'] = 1994
    assert fund.totalDeColisoes == 3

    fund['ibm'] = 1911
    fund['htc'] = 1997
    assert fund.totalDeColisoes == 4


def testes_aPropiedade_totalDeColisoes_naoSeraInfluenciadaPelasSubstituicoesDosValoresDasCahves():
    cronometro = TabelaHash(lambda texto: len(texto))

    cronometro['segundos'] = 0
    cronometro['segundos'] = 1
    cronometro['segundos'] = 2

    assert cronometro.totalDeColisoes == 0


def testes_operador_del():
    fund = dataDaFundacaoDeGrandesEmpresas()

    del fund['microsoft']
    assert 'microsoft' not in fund
    assert 'google' in fund
    assert 'apple' in fund
    assert 'facebook' in fund
    assert 'ibm' in fund

    del fund['google']
    assert 'google' not in fund
    assert 'apple' in fund
    assert 'facebook' in fund
    assert 'ibm' in fund

    del fund['apple']
    assert 'apple' not in fund
    assert 'facebook' in fund
    assert 'ibm' in fund

    del fund['facebook']
    assert 'facebook' not in fund
    assert 'ibm' in fund

    del fund['ibm']
    assert 'ibm' not in fund


def testes_propiedade_tamanho_aposRemoverAlgunsItens():
    fund = dataDaFundacaoDeGrandesEmpresas()

    del fund['microsoft']
    del fund['google']
    assert fund.tamanho == 3

    del fund['apple']
    assert fund.tamanho == 2

    del fund['facebook']
    del fund['ibm']
    assert fund.tamanho == 0


def testes_oOperador_del_iraGerarUmErroSeAChaveNaoForLocalizada():
    with raises(ItemNaoEncontrado):
        del fundacao['fox']


def testes_tabelaHashComUmaFuncaoQueGeraCodigosNegativos():
    fund = TabelaHash(lambda empresa: -len(empresa))

    fund['microsoft'] = 1975
    fund['google'] = 1998
    fund['apple'] = 1976
    fund['facebook'] = 2004
    fund['ibm'] = 1911

    assert 'microsoft' in fund
    assert 'google' in fund
    assert 'apple' in fund
    assert 'facebook' in fund
    assert 'ibm' in fund
