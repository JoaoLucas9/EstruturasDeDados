class naoGeraErro:
    """Gerenciador de contexto voltado para testes que visa garantir que um
    trecho de código não gera nenhum erro.

    Exceções
       :exception ErroInesperadoErro se o código que está sendo testado
       lançar qualquer erro/exceção.
    """

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        algumErroFoiLancado = all((exc_type, exc_val, exc_tb))

        if algumErroFoiLancado:
            raise ErroInesperado(exc_type)


class ErroInesperado(Exception):
    """Erro gerado pelo gerenciador de contexto 'naoLancaErro' quando o
    código sob teste gera um erro.
    Uma instância desta classe indica que o código gera um erro quando não
    deveria.
    """

    def __init__(self, tipoDaExcecao):
        tipoDaExcecao = str(tipoDaExcecao)
        tipoDaExcecao = tipoDaExcecao[7:]

        super().__init__(f'Foi gerado um {tipoDaExcecao[:-1]}.')


