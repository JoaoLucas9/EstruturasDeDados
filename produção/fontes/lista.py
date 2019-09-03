from collections.abc import Iterable
from colecoes.colecoes import ocorrencias
from colecoes.colecoes import contemDuplicados


_VINTE_TRILHOES = 20000000000000


def eIteravel(obj) -> bool:
    """Verifica se o objeto é iterável.

       Parâmetros:
          obj :

       Retorno: true se o objeto for iterável, false caso contrário.
    """
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def _intervalo(param):
    if isinstance(param, int):
        return range(param, param + 1)

    if param.endswith('+'):
        return range(int(param.strip('+')), _VINTE_TRILHOES)
    return range(-_VINTE_TRILHOES, int(param.strip('-')) + 1)


def _iteravel(obj):
    return obj if isinstance(obj, (list, tuple, set)) else [obj]


class Lista:

    DUPLICADOS = 'CONSTANTE_CLASSE_LISTA_HASH_001H'

    # constante para determinar o comportamento do método
    # contem(iteravel, operador, dicio).
    OU = 'ou'

    def __init__(self):
        self._lista = []

    # TODO o operador + deve aceitar também os seguintes tipos:
    # Lista
    # Set
    # 'num * [T | list | Lista | Set]',
    # ex.: '2 * 4', adiciona 2 números 4 ( op)
    def __add__(self, elemento):
        """ Anexa o elemento a lista.

            Cenários:
               elemento : T -> o elemento será anexado no fim da lista

               elemento : list -> os itens da lista serão anexados ao fim desta,
               na ordem na qual são encontrados. Exemplo:
                  lista = Lista()
                  lista + 1; lista + 2; lista + 3
                  lista + [4, 5]

                  lista final = [1, 2, 3, 4, 5]

           Parâmetros:
              elemento : [T | list] -> o elemento que será anexado.

           Retorno:
              a lista atualizada.
        """
        if isinstance(elemento, list):
            self._lista += elemento
        else:
            self._lista.append(elemento)

        return self

    def __contains__(self, obj) -> bool:
        """Determina se um ou mais objetos estão na Lista.

        Retorno:

           1) se informado um objeto iterável: retorna true se todos os
           itens do iterável forem encontrados na Lista, false caso
           contrário.
           A ordem, o espaçamento entre os objetos e o total de
           ocorrências são irrelevantes, exemplos, considere a Lista L1
           [1, 2, 3, 4]:

           [3, 2, 1] in L1 retorna true, a ordem dos objetos no iterável e
           na Lista é irrelevante.

           [1, 4] in L1 retorna true, o espaçamento dos objetos é
           irrelevante (o 4 em L1 não vem logo após o 1).

           [1, 1, 1] in L1 retorna true, há 3 1s na list da esquerda
           contudo apenas 1 1 na Lista, o total de ocorrências dos objetos é
           irrelevante.

           Resumindo, este método preocupa-se apenas em verificar se um
           objeto está ou não na Lista.

           2) se informada a constante DUPLICADOS: retorna true se houver
           um ou mais itens duplicados, false caso não haja nenhum.

           3) se informado um objeto não iterável e diferente de DUPLICADOS:
           retorna true se o estiver for encontrado na Lista, false caso
           contrário

        """
        if obj is self.DUPLICADOS:
            return contemDuplicados(self._lista)

        if not eIteravel(obj):
            return obj in self._lista

        for x in obj:
            if x not in self._lista:
                return False

        return True

    def _contemUmaSequenciaDeItensIdenticaAo(self, iteravel: Iterable):
        try:
            primeiroItemDoIteravel= iter(iteravel).__next__()
        except StopIteration:
            return True

        for indice in ocorrencias(primeiroItemDoIteravel, self._lista):

            for i, v in enumerate(iteravel, indice):
                if i == len(self._lista) or self._lista[i] != v:
                    break
            else:
                return True

        return False


    # TODO é um bom nome ?
    # TODO rmover 1º if
    def _satisfazTodasAsCondicoesDoBack(self, dicio:dict):
        if dicio is None:
            return True

        for chave in dicio: # TODO alterar nome variável chave

            ocorrencias = self._lista.count(dicio[chave])

            if isinstance(chave, int):
                if ocorrencias != chave:
                    return False
                continue

            if chave.endswith('+'):
                if ocorrencias < int(chave.strip('+')):
                    return False
                continue

            if ocorrencias > int(chave.strip('-')):
                return False

        return True


    def _satisfazTodasAsCondicoesDoBack2(self, dicio:dict):
        if dicio is None:
            return True

        for chave in dicio: # TODO alterar nome variável chave

            ocorrencias = self._lista.count(dicio[chave])

            if ocorrencias not in _intervalo(chave):
                return False

        return True


    def _satisfazTodasAsCondicoesDo(self, dicio:dict):
        if dicio is None:
            return True

        for c, v in dicio.items(): # TODO alterar nome variável chave

            for valor in _iteravel(v):
                intervalo = _intervalo(c)
                if self._lista.count(valor) not in intervalo:
                    return False

        return True


    # TODO alterar o valor padrão de dicio para um  dict imutável e vazio,
    #  padrão singleton
    def contem(self, iteravel:Iterable=(), operador:str='e', dicio:dict=None) \
            -> bool:
        """
        Determina se uma sequência e/ou uma determinada quantidade de objetos
        podem ser encontradas na Lista.

        Cenários:
           1) se o iterável tiver sido informado: o método irá procurar por
           uma sequência de objetos exatamente igual ao iterável.

           2) se o dicio tiver sido informado: verifica se todas as
           condições foram satisfeitas.
           Condição = par chave-valor, a chave pode ser um int ou uma str,
           o valor pode ser qualquer objeto.
           Se a chave for uma str ela deve seguir o padrão x+/-, onde x é um
           número seguido do sinal + ou -.
           Caso a chave seja um int para a condição ser considerada como
           satisfeita a quantidade de ocorrências do valor na Lista deve ser
           igual a sua chave, caso a chave seja uma str x+, então a
           quantidade de ocorrências do valor na Lista deve ser maior igual
           a x (x é a menor quantidade de ocorrências permitida), se a chave
           for uma str x-, então a quantidade de ocorrências do valor deve
           ser menor igual x (x é a maior quantidade de ocorrências permitida).
           Se o valor de uma par chave-valor for um list, tuple ou set então
           serão verificados todos os objetos contidos na coleção, um por
           um, exemplo, para que a condição 1:[2, 3] seja satisfeita os
           números 2 e 3 deverão aparecer uma única vez em self.
           OBS.: a ordem dos números, bem como a distância entre eles em
           self não importa, basta que eles aparecam uma só vez.


        Parâmetros:
           iteravel

           operador -> determina o comportamento do método, veja o cenário
           número 3 na seção Retorna.
           Pode assumir dois valores, o padrão ou a constante Lista.OU.

           dicio

        Retorna:
           1) apenas o iterável foi informado: true se for encontrada uma
           sequência de objetos exatamente igual ao iterável, false caso a
           sequência não seja encontrada.

           2) apenas o dicio foi informado: true se todas as condições forem
           satisfeitas, false caso ao menos uma delas não seja satisfeita.

           3) o iterável e o dicio foram informados:
              3.1) se o operador não tiver sido informado: true se for
              encontrada uma sequência de objetos exatamente igual ao
              iterável e se todas as condições do dicio forem satisfeitas,
              false caso as condições acima não sejam satisfeitas.

              3.2) se o operador for OU: true se for encontrada uma sequência
              de objetos exatamente igual ao iterável ou se todas as condições
              do dicio forem satisfeitas, false caso nenhuma das condições
              anteriores seja satisfeita.
        """
        if operador == 'e':
            return self._contemUmaSequenciaDeItensIdenticaAo(iteravel) and \
                self._satisfazTodasAsCondicoesDo(dicio)

        return self._contemUmaSequenciaDeItensIdenticaAo(iteravel) or \
                self._satisfazTodasAsCondicoesDo(dicio)
