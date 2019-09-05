"""Gerenciador de contexto para suprir uma deficiência framework de testes
pytest, que não fornece uma maneira de garantir que um trecho de código não
gera erro.

Este módulo tem por objetivo fornece classes e funções que estendem as
funcionalidades do pytest.

Novas funções e classes serão adicionadas em versões futuras.

Autor: João Lucas Alves Almeida Santos
Versão: 0.1
"""

class naoGeraErro:
    """Gerenciador de contexto voltado para testes que visa garantir que um
    trecho de código não gera nenhum erro.
    """

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exceções
            :exception ErroInesperadoErro se o código que está sendo testado
            gerar um erro.
        """
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


