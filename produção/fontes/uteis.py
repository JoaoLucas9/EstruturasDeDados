NAO_INFORMADO = 'valor não informado Recife_PE 26/08/2019 14:35'
INDEFINIDO = 'valor não definido Recife_PE 30/08/2019 07:08'
INFINITO = float('inf')


def executar(funcao, padrao=None):
    """Executa a função informada e retorna o valor retornado pela mesma se
    nenhum erro for gerado.
    Se a função gerar algum erro ao ser executada, então será retornado o
    valor padrão.

    Parâmetros:
       :param funcao : Callable não deve receber nenhum parâmetro.

       :param padrao o valor que será retornado se a função gerar algum erro.

    """
    try:
        o = funcao()
        return o
    except Exception:
        return padrao


class IteradorVazio:


    def __iter__(self):
        return self


    def __next__(self):
        raise StopIteration


