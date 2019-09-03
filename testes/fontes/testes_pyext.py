from pyext import naoGeraErro, ErroInesperado
from pytest import raises, fail

def testes_oGerenciadorDeContexto_naoLancaErro():
    lancaraUmErroSeOBlocoDeCodigoLancarUmErro()
    naoLancaraUmErroSeOBlocoDeCodigoNaoLancarNenhumErro()


def lancaraUmErroSeOBlocoDeCodigoLancarUmErro():
    with raises(ErroInesperado), naoGeraErro():
        raise Exception


def naoLancaraUmErroSeOBlocoDeCodigoNaoLancarNenhumErro():
    try:
        with naoGeraErro():
            1 + 1
    except ErroInesperado:
        fail('Nenhum erro deveria ser gerado.')


